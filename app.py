"""
Quantium Hire-to-Onboard AI Swarm — local web interface.

Streams live swarm events via Server-Sent Events so you can watch the
specialist threads fan out in real-time.

Usage:
    pip install flask anthropic python-dotenv
    export ANTHROPIC_API_KEY="sk-ant-..."
    python app.py
    # then open http://localhost:5000
"""

import json
import logging
import os
from pathlib import Path

from anthropic import Anthropic
from flask import Flask, Response, abort, render_template, request, stream_with_context

# Security: structured logging — never log sensitive values (API keys, tokens, PII)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security: disable debug mode and exception propagation — prevents stack-trace
# exposure to clients (OWASP A05: Security Misconfiguration)
app.config.update(
    DEBUG=False,
    TESTING=False,
    PROPAGATE_EXCEPTIONS=False,
)

SYNTHETIC_DIR = Path("synthetic-data")

# Security: hardcoded allowlist of valid profiles — any filename not in this set
# is rejected before any filesystem access (prevents path traversal, CWE-22)
PROFILES = [
    {
        "filename": "new-hire-callum-price.md",
        "name": "Callum Price",
        "initials": "CP",
        "role": "Office Manager",
        "level": "Associate (A2)",
        "team": "Business Operations — London",
        "start": "2026-06-30",
        "start_label": "30 Jun 2026",
        "days_to_start": 14,
        "location": "London, Cannon Street (5 days/week)",
        "urgency": "high",
        "urgency_label": "14 days — urgent",
    },
    {
        "filename": "new-hire-priya-mehta.md",
        "name": "Priya Mehta",
        "initials": "PM",
        "role": "Senior AI Consultant",
        "level": "Principal Consultant (PC)",
        "team": "AI & Data Practice",
        "start": "2026-07-07",
        "start_label": "7 Jul 2026",
        "days_to_start": 21,
        "location": "Remote-first / London ~4 days/month",
        "urgency": "medium",
        "urgency_label": "21 days",
    },
    {
        "filename": "new-hire-claire-holloway.md",
        "name": "Claire Holloway",
        "initials": "CH",
        "role": "Vice President, Retail Solutions",
        "level": "Vice President (VP)",
        "team": "Retail & Consumer Practice",
        "start": "2026-07-14",
        "start_label": "14 Jul 2026",
        "days_to_start": 28,
        "location": "London hybrid + client travel up to 40%",
        "urgency": "low",
        "urgency_label": "28 days",
    },
]

# Security: O(1) set lookup for allowlist validation
VALID_FILENAMES: set[str] = {p["filename"] for p in PROFILES}


@app.after_request
def apply_security_headers(response: Response) -> Response:
    """Apply OWASP-recommended security headers to every response."""
    # Prevent MIME-type sniffing (CWE-16 / OWASP A05)
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Prevent clickjacking (OWASP A05)
    response.headers["X-Frame-Options"] = "DENY"
    # Limit referrer leakage
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # Disable browser features not required by this tool
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    # CSP: restrict resource origins; 'unsafe-inline' for styles is acceptable
    # in this localhost dev context — tighten for production deployments
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "font-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'"
    )
    return response


@app.route("/")
def index() -> str:
    # Security: Jinja2 auto-escaping is enabled by default for .html templates;
    # all {{ variables }} are HTML-escaped (prevents XSS, CWE-79)
    return render_template("index.html", profiles=PROFILES)


@app.route("/run", methods=["POST"])
def run_onboarding() -> Response:
    """Accept a profile selection and stream swarm events as SSE."""
    # Security: enforce JSON content type before parsing the body
    if not request.is_json:
        abort(415)

    body = request.get_json(silent=True)
    if not body or not isinstance(body, dict):
        abort(400)

    # Security: validate filename against allowlist before any filesystem access
    # (prevents path traversal CWE-22; deny-by-default access control)
    filename = body.get("profile", "")
    if not isinstance(filename, str) or filename not in VALID_FILENAMES:
        # Truncate in log to prevent log injection (CWE-117)
        logger.warning("Rejected invalid profile request: %.80r", filename)
        abort(400)

    profile_path = SYNTHETIC_DIR / filename

    # Security: defence-in-depth — verify resolved path stays within SYNTHETIC_DIR
    # even though the filename was already validated against the allowlist
    try:
        resolved = profile_path.resolve()
        base = SYNTHETIC_DIR.resolve()
        if not resolved.is_relative_to(base):
            logger.warning("Path traversal attempt blocked: %s", resolved)
            abort(400)
    except (ValueError, OSError):
        abort(400)

    if not profile_path.exists():
        abort(404)

    def generate():
        # Security: API key sourced from environment only — never hardcoded (CWE-798)
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            # Generic error to client; detail stays in server logs (OWASP A09)
            logger.error("ANTHROPIC_API_KEY is not set in the environment")
            yield _sse({"type": "error", "text": "Server configuration error. Contact the administrator."})
            return

        coordinator_id_path = Path(".coordinator_id")
        environment_id_path = Path(".environment_id")

        if not coordinator_id_path.exists() or not environment_id_path.exists():
            yield _sse({
                "type": "error",
                "text": (
                    "Swarm not initialised. Run setup_environment.py, "
                    "create_specialists.py, upload_skills.py, and "
                    "create_coordinator.py first."
                ),
            })
            return

        coordinator_id = coordinator_id_path.read_text().strip()
        environment_id = environment_id_path.read_text().strip()

        if not coordinator_id or not environment_id:
            yield _sse({"type": "error", "text": "Invalid coordinator or environment configuration."})
            return

        profile_text = profile_path.read_text(encoding="utf-8")

        client = Anthropic(
            api_key=api_key,  # Security: from env — never logs this value
            default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
        )

        user_message = (
            "A new hire's profile has just landed and their start date is fixed. "
            "Please run the standard onboarding process:\n"
            "1. Read the new-hire profile yourself.\n"
            "2. Delegate to all four specialists in parallel.\n"
            "3. Synthesise their replies.\n"
            "4. Produce the final day-1 readiness pack as a structured markdown document.\n\n"
            "Specialists have their own skills attached for their respective domains. "
            "Move fast — the start date is fixed.\n\n"
            f"=====  DOCUMENT: {filename}  =====\n{profile_text}"
        )

        try:
            session = client.beta.sessions.create(
                agent=coordinator_id,
                environment_id=environment_id,
                title=f"Onboarding — {filename.replace('.md', '')}",
            )

            # Security: session ID is a resource identifier — safe to emit to client
            yield _sse({"type": "session_created", "session_id": session.id})
            logger.info("Session created: %s for profile: %s", session.id, filename)

            final_parts: list[str] = []

            with client.beta.sessions.events.stream(session.id) as stream:
                client.beta.sessions.events.send(
                    session.id,
                    events=[{
                        "type": "user.message",
                        "content": [{"type": "text", "text": user_message}],
                    }],
                )
                for event in stream:
                    t = event.type
                    if t == "session.thread_created":
                        yield _sse({"type": "thread_created", "agent": getattr(event, "agent_name", "Unknown")})
                    elif t == "session.thread_status_running":
                        yield _sse({"type": "thread_running", "agent": getattr(event, "agent_name", "Unknown")})
                    elif t == "agent.thread_message_sent":
                        yield _sse({"type": "delegate", "to": getattr(event, "to_agent_name", "Unknown")})
                    elif t == "agent.thread_message_received":
                        yield _sse({"type": "reply", "from_agent": getattr(event, "from_agent_name", "Unknown")})
                    elif t == "agent.tool_use":
                        yield _sse({"type": "tool", "name": getattr(event, "name", "Unknown")})
                    elif t == "agent.message":
                        for block in event.content:
                            if getattr(block, "type", None) == "text":
                                final_parts.append(block.text)
                                yield _sse({"type": "text_chunk", "text": block.text})
                    elif t == "session.status_idle":
                        yield _sse({"type": "done", "session_id": session.id})
                        logger.info("Swarm finished for session: %s", session.id)
                        break

            # Persist transcript
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            transcript_path = output_dir / f"transcript-{filename.replace('.md', '')}.txt"
            transcript_path.write_text("".join(final_parts), encoding="utf-8")
            logger.info("Transcript saved: %s", transcript_path)

        except Exception:
            # Security: full exception in server logs; generic message to client
            # (prevents internal path/library disclosure — OWASP A05)
            logger.exception("Error running onboarding swarm for profile: %s", filename)
            yield _sse({"type": "error", "text": "An error occurred. Please check the server logs."})

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-store",
            "X-Accel-Buffering": "no",  # disable nginx/proxy buffering for SSE
            "Connection": "keep-alive",
        },
    )


def _sse(payload: dict) -> str:
    """Format a dict as an SSE data line."""
    return f"data: {json.dumps(payload)}\n\n"


if __name__ == "__main__":
    # Security: bind to loopback only — never expose to 0.0.0.0 for local dev tools
    app.run(host="127.0.0.1", port=5000, debug=False)
