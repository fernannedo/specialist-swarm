"""
Run the Hire-to-Onboard swarm against the synthetic new-hire profile.

Inlines the new-hire profile (+ any supporting HR files) into the user message
(simpler than Files API for hackathon-scale content). Streams events as they
come in so you can watch the parallel thread fan-out — this is the demo,
narrate it live.

Saves the final transcript to outputs/.

Usage:
    python run_deal_desk.py                              # first new-hire-*.md
    python run_deal_desk.py new-hire-priya-mehta.md      # a specific profile
"""

import os
import sys
from pathlib import Path

from anthropic import Anthropic


SYNTHETIC_DIR = Path("synthetic-data")
# Anne owns synthetic-data/. Add supporting HR files here as she creates them
# (e.g. team roster, buddy pool, equipment catalog). Kept explicit (not a glob
# of synthetic-data/) so we never feed stale Deal Desk files into the swarm.
SUPPORTING_FILES: list[Path] = []
OUTPUT_DIR = Path("outputs")


def resolve_profile() -> Path:
    """Pick the new-hire profile to run.

    Optional CLI arg selects a specific profile (a path, or a bare filename
    under synthetic-data/). With no arg, default to the first new-hire-*.md.
    """
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        candidate = arg if arg.exists() else SYNTHETIC_DIR / arg.name
        if not candidate.exists():
            raise SystemExit(f"Profile not found: {sys.argv[1]}")
        return candidate

    profiles = sorted(SYNTHETIC_DIR.glob("new-hire-*.md"))
    if not profiles:
        raise SystemExit(
            f"No new-hire profile found in {SYNTHETIC_DIR}/ "
            "(expected a file like new-hire-*.md)."
        )
    if len(profiles) > 1:
        print(f"  available profiles: {[p.name for p in profiles]}")
        print(f"  using {profiles[0].name} "
              "(pass a filename as an arg to pick another)")
    return profiles[0]


def load_inputs_as_context(profile_path: Path) -> str:
    blocks = []
    for path in [profile_path, *SUPPORTING_FILES]:
        if not path.exists():
            print(f"  WARNING: {path} missing — skipping")
            continue
        print(f"  including {path.name}")
        blocks.append(f"=====  DOCUMENT: {path.name}  =====\n{path.read_text()}")
    return "\n\n".join(blocks)


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running.")

    if not Path(".coordinator_id").exists() or not Path(".environment_id").exists():
        raise SystemExit(
            "Missing .coordinator_id or .environment_id. Run "
            "setup_environment.py, create_specialists.py, upload_skills.py, "
            "then create_coordinator.py first."
        )

    coordinator_id = Path(".coordinator_id").read_text().strip()
    environment_id = Path(".environment_id").read_text().strip()

    client = Anthropic()

    profile_path = resolve_profile()
    print(f"Loading new-hire profile ({profile_path.name}) + supporting docs...")
    context = load_inputs_as_context(profile_path)

    print(f"\nStarting session against coordinator {coordinator_id}...")
    session = client.beta.sessions.create(
        agent=coordinator_id,
        environment_id=environment_id,
        title="Onboarding — new hire day-1 readiness",
    )
    Path(".last_session_id").write_text(session.id)

    user_message = (
        "A new hire's profile has just landed and their start date is fixed. "
        "Please run the standard onboarding process:\n"
        "1. Read the new-hire profile yourself.\n"
        "2. Delegate to all four specialists in parallel.\n"
        "3. Synthesise their replies.\n"
        "4. Produce the final day-1 readiness pack as a branded Word document "
        "if you have access to a docx skill; otherwise output the pack "
        "as a structured markdown document.\n\n"
        "Specialists have their own skills attached for their respective "
        "domains. Move fast — the start date is fixed.\n\n"
        f"{context}"
    )

    # Stream the events — this is the demo. Watch for parallel thread spawns.
    print("\n=== EVENT STREAM (this is the demo) ===\n")
    final_text_parts: list[str] = []

    with client.beta.sessions.events.stream(session.id) as stream:
        client.beta.sessions.events.send(
            session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": user_message}],
                }
            ],
        )
        for event in stream:
            t = event.type
            if t == "session.thread_created":
                print(f"  [thread spawned]   {event.agent_name}", flush=True)
            elif t == "session.thread_status_running":
                name = getattr(event, "agent_name", "?")
                print(f"  [thread running]   {name}", flush=True)
            elif t == "agent.thread_message_received":
                print(f"  [reply ←]          {event.from_agent_name}", flush=True)
            elif t == "agent.thread_message_sent":
                print(f"  [delegate →]       {event.to_agent_name}", flush=True)
            elif t == "agent.message":
                for block in event.content:
                    if getattr(block, "type", None) == "text":
                        final_text_parts.append(block.text)
                        print(block.text, end="", flush=True)
            elif t == "agent.tool_use":
                print(f"\n  [tool: {getattr(event, 'name', '?')}]", flush=True)
            elif t == "session.status_idle":
                print("\n\n[swarm finished]")
                break

    OUTPUT_DIR.mkdir(exist_ok=True)
    transcript_path = OUTPUT_DIR / "coordinator-transcript.txt"
    transcript_path.write_text("".join(final_text_parts))
    print(f"\nCoordinator transcript saved to {transcript_path}")

    # Pull every file the agents produced in the container
    print("\nDownloading deliverables from the session container...")
    files = client.beta.files.list(
        scope_id=session.id,
        betas=["managed-agents-2026-04-01"],
    )
    file_count = 0
    for f in files.data:
        out_path = OUTPUT_DIR / f.filename
        print(f"  {f.filename}  ->  {out_path}")
        content = client.beta.files.download(f.id)
        content.write_to_file(str(out_path))
        file_count += 1

    if file_count == 0:
        print("  (no files found — agents may have produced text-only output)")
    else:
        print(f"\nDownloaded {file_count} file(s) to {OUTPUT_DIR}/")

    print(f"\nView the full session (including all sub-agent threads) at:")
    print(f"  https://platform.claude.com/sessions/{session.id}")


if __name__ == "__main__":
    main()
