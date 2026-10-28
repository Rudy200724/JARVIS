from __future__ import annotations

from datetime import datetime

from tools.applications import open_application, refresh_applications


def execute_command(text: str) -> str | None:
    """
    Temporary command parser.

    This keeps your current JARVIS working while we build the proper
    LLM -> structured tool-call router in the next backend phase.
    """
    cleaned = text.lower().strip().rstrip(".!?")

    if cleaned.startswith("open "):
        app = cleaned.removeprefix("open ").strip()

        if app:
            return open_application(app)

    if cleaned in {
        "refresh apps",
        "refresh applications",
        "rescan apps",
        "rescan applications",
    }:
        return refresh_applications()

    if (
        "what is the time" in cleaned
        or "what's the time" in cleaned
        or "current time" in cleaned
    ):
        now = datetime.now()
        return now.strftime(
            "Today is %A, %d %B %Y and the time is %I:%M %p, Sir."
        )

    return None
