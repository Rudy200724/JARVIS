from __future__ import annotations

import re
from datetime import datetime

from tools.applications import open_application, refresh_applications


def execute_command(text: str) -> str | None:
    """
    Command parser for system and device actions.
    Interprets user intent for opening apps, rescanning apps, and querying system status.
    """
    cleaned = text.lower().strip().rstrip(".!?,")

    # Time queries
    if (
        "what is the time" in cleaned
        or "what's the time" in cleaned
        or "current time" in cleaned
        or cleaned == "time"
    ):
        now = datetime.now()
        return now.strftime(
            "Today is %A, %d %B %Y and the time is %I:%M %p, Sir."
        )

    # Refresh/rescan applications
    if cleaned in {
        "refresh apps",
        "refresh applications",
        "rescan apps",
        "rescan applications",
        "reload apps",
        "reload applications",
    }:
        return refresh_applications()

    # Application opening patterns
    # Matches natural phrases like:
    # - "open spotify"
    # - "please open chrome"
    # - "can you open vscode"
    # - "launch discord"
    # - "start calculator"
    # - "run notepad"
    # - "open up vs code"
    # - "open the file explorer"
    open_pattern = re.compile(
        r"^(?:please\s+)?(?:can\s+you\s+|could\s+you\s+|would\s+you\s+)?(?:open|launch|start|run)(?:\s+up)?(?:\s+(?:the|a|an))?\s+(.+?)(?:\s+please|\s+for\s+me)?$",
        re.IGNORECASE,
    )
    match = open_pattern.match(cleaned)
    if match:
        app = match.group(1).strip()
        if app:
            return open_application(app)

    return None
