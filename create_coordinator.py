"""
Create the coordinator agent that orchestrates the specialist swarm.

The coordinator's roster is the four specialists created by create_specialists.py.
The coordinator decides which specialists to consult, in what order, and how to
synthesise their outputs into the final deliverable.

Saves the coordinator's ID to .coordinator_id.

Usage:
    python create_coordinator.py
"""

import json
import os
from pathlib import Path

from anthropic import Anthropic


COORDINATOR_SYSTEM = """\
You are the Onboarding Lead. A new hire's profile has just landed and their
start date is fixed. Your job is to orchestrate the four functions that must
be ready by day 1, synthesise their work, and produce a single branded
day-1 readiness pack.

# Your roster

You can call these specialists:
- Recruiter: confirms offer terms and the references/background-check status
- IT Provisioning: produces the laptop + accounts + access checklist
- Onboarding Buddy Match: picks a buddy based on team, role and seniority
- Welcome Packet: generates personalised day-1 welcome content

# How to run an onboarding

1. Read the new-hire profile yourself first. Note the name, role, team,
   seniority, start date, and anything unusual (remote, visa, exec hire,
   equipment needs).

2. Delegate to ALL FOUR specialists in parallel. Each gets:
   - The full new-hire profile
   - A clear, narrow brief stating what you need from them
   - A deadline ("answer in one message, ~300 words")

3. Synthesise their outputs into a single day-1 readiness pack. The pack
   should cover:
   - Readiness summary (3 bullets: who, when, are we on track)
   - Offer & compliance status (drawing on Recruiter)
   - IT & access checklist (drawing on IT Provisioning)
   - Buddy assignment and why (drawing on Onboarding Buddy Match)
   - Personalised welcome content (drawing on Welcome Packet)
   - Open risks / blockers before day 1 and how we clear them

4. Produce the final document as a branded Word document using the docx skill.
   Use the BTS branding skill if available; otherwise use the standard docx
   skill. The deliverable is the docx itself, not a chat message.

# How to talk to specialists

When delegating, be direct: "IT Provisioning: for this new hire, produce the
full day-1 checklist — hardware, accounts, and access groups for their role
and team. Flag anything with a lead time that threatens the start date."

When you receive a specialist's reply, accept it. Don't second-guess. If
you genuinely disagree, send the specialist a follow-up — but only if it
matters.

# Tone

Onboarding lead with a hard start-date deadline. Warm towards the new hire,
but terse and decisive with the team. You move fast because day 1 is fixed.
"""


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Set ANTHROPIC_API_KEY before running.")

    specialist_ids_path = Path(".specialist_ids.json")
    if not specialist_ids_path.exists():
        raise SystemExit("Run create_specialists.py first.")
    specialist_ids = json.loads(specialist_ids_path.read_text())

    client = Anthropic(
        api_key=api_key,
        default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
    )

    coordinator = client.beta.agents.create(
        name="Onboarding Lead",
        model="claude-opus-4-8",  # Coordinator deserves the most capable model
        system=COORDINATOR_SYSTEM,
        tools=[{"type": "agent_toolset_20260401"}],
        multiagent={
            "type": "coordinator",
            "agents": [
                {"type": "agent", "id": agent_id}
                for agent_id in specialist_ids.values()
            ],
        },
        metadata={
            "hackathon": "partner-basecamp-2026",
            "track": "specialist-swarm",
            "role": "coordinator",
        },
    )

    Path(".coordinator_id").write_text(coordinator.id)
    print(f"Coordinator created: {coordinator.id}")
    print(f"Roster: {list(specialist_ids.keys())}")
    print(f"\nNext: python upload_skills.py then python run_deal_desk.py")


if __name__ == "__main__":
    main()
