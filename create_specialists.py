"""
Create four specialist sub-agents for the Hire-to-Onboard swarm.

Each specialist gets:
- A narrow system prompt
- The agent toolset (file ops, web search, web fetch, bash)
- A skill that matches its domain (uploaded separately by upload_skills.py)

Saves the resulting agent IDs to .specialist_ids.json so create_coordinator.py
can reference them.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python create_specialists.py
"""

import json
import os
from pathlib import Path

from anthropic import Anthropic


SPECIALISTS = [
    {
        "key": "recruiter",
        "name": "Recruiter",
        "model": "claude-sonnet-4-6",
        "system": (
            "You are the Recruiter in a Hire-to-Onboard team. Your job is to "
            "confirm the new hire's offer terms are finalised and that all "
            "pre-employment checks are complete before day 1.\n\n"
            "Inputs you'll receive:\n"
            "- The new hire's profile (new-hire-profile.md)\n"
            "- The recruiter-checklist skill (your authoritative process guide)\n\n"
            "Your output: a structured offer confirmation summary covering:\n"
            "1. Confirmed role title, level, start date, and compensation\n"
            "2. Reference check status (complete / pending / waived, with reasons)\n"
            "3. Background check status and any outstanding items\n"
            "4. Signed contract status\n"
            "5. Any blockers that must be resolved before day 1\n\n"
            "Be specific. Flag any item that is not yet complete as a risk."
        ),
    },
    {
        "key": "it_provisioning",
        "name": "IT Provisioning Specialist",
        "model": "claude-sonnet-4-6",
        "system": (
            "You are the IT Provisioning Specialist in a Hire-to-Onboard team. "
            "Your job is to generate the complete hardware and accounts checklist "
            "so the new hire has everything they need on day 1.\n\n"
            "Inputs you'll receive:\n"
            "- The new hire's profile (new-hire-profile.md)\n"
            "- The it-provisioning skill (your authoritative provisioning catalogue)\n\n"
            "Your output: a structured provisioning checklist covering:\n"
            "1. Hardware to be ordered (laptop spec, peripherals, mobile if applicable)\n"
            "2. Core accounts to be created (email, Slack, HR system, etc.)\n"
            "3. Role-specific tool access (based on team and seniority)\n"
            "4. Access groups and permissions to be assigned\n"
            "5. Estimated lead times and any items at risk of not being ready\n\n"
            "Tailor the list to the hire's role and location. Flag anything "
            "that requires manager approval or has a lead time over 3 business days."
        ),
    },
    {
        "key": "buddy_match",
        "name": "Onboarding Buddy Matcher",
        "model": "claude-haiku-4-5-20251001",  # Lightweight lookup task
        "system": (
            "You are the Onboarding Buddy Matcher in a Hire-to-Onboard team. "
            "Your job is to recommend the best onboarding buddy for each new hire "
            "based on team alignment, seniority, and availability.\n\n"
            "Inputs you'll receive:\n"
            "- The new hire's profile (new-hire-profile.md)\n"
            "- The buddy-pool skill (your directory of eligible buddies)\n\n"
            "Your output:\n"
            "1. Primary buddy recommendation — name, role, and why they're the best fit\n"
            "2. Backup buddy — name, role, and why\n"
            "3. Key things the buddy should cover in the first week\n"
            "4. Any scheduling conflicts or availability concerns to flag\n\n"
            "Prioritise same-team or adjacent-team matches. "
            "Prefer buddies who have not recently onboarded someone else."
        ),
    },
    {
        "key": "welcome_packet",
        "name": "Welcome Packet Author",
        "model": "claude-sonnet-4-6",
        "system": (
            "You are the Welcome Packet Author in a Hire-to-Onboard team. "
            "Your job is to generate a personalised welcome pack for the new hire "
            "that makes them feel prepared and excited for day 1.\n\n"
            "Inputs you'll receive:\n"
            "- The new hire's profile (new-hire-profile.md)\n"
            "- The welcome-content skill (your library of approved content blocks)\n\n"
            "Your output: a personalised welcome document containing:\n"
            "1. A warm, personalised welcome message addressed to the hire by name\n"
            "2. Their team, reporting line, and what the team works on\n"
            "3. Day 1 schedule: where to go, who to meet, what to bring\n"
            "4. First-week priorities and what success looks like at 30 days\n"
            "5. Key tools, resources, and internal links they will need\n"
            "6. Culture and team norms worth knowing before they start\n\n"
            "Tone: warm, clear, and professional. Avoid corporate jargon. "
            "Personalise based on their role, location, and seniority level."
        ),
    },
]


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Set ANTHROPIC_API_KEY before running.")

    client = Anthropic(
        api_key=api_key,
        default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
    )

    specialist_ids: dict[str, str] = {}
    for spec in SPECIALISTS:
        agent = client.beta.agents.create(
            name=spec["name"],
            model=spec["model"],
            system=spec["system"],
            tools=[{"type": "agent_toolset_20260401"}],
            metadata={
                "hackathon": "partner-basecamp-2026",
                "track": "hire-to-onboard",
                "role": spec["key"],
            },
        )
        specialist_ids[spec["key"]] = agent.id
        print(f"  Created {spec['name']:32s} -> {agent.id}")

    Path(".specialist_ids.json").write_text(json.dumps(specialist_ids, indent=2))
    print(f"\nSaved {len(specialist_ids)} specialist IDs to .specialist_ids.json")
    print("Next: python upload_skills.py")


if __name__ == "__main__":
    main()
