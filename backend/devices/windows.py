from __future__ import annotations

import json
import os
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path

from devices.base import Application, Device


class WindowsDevice(Device):
    """
    Discovers and launches Windows applications without maintaining
    a hard-coded application dictionary.

    Discovery sources:
      1. Current-user Start Menu shortcuts
      2. All-users Start Menu shortcuts
      3. Windows Get-StartApps catalogue

    Results are kept in memory for fast repeated launches.
    """

    def __init__(self) -> None:
        self._applications: list[Application] = []
        self.refresh_applications()

    @staticmethod
    def _normalise(value: str) -> str:
        value = value.lower().strip()
        value = re.sub(r"[^a-z0-9]+", " ", value)
        return " ".join(value.split())

    def _start_menu_folders(self) -> list[Path]:
        folders: list[Path] = []

        appdata = os.environ.get("APPDATA")
        programdata = os.environ.get("PROGRAMDATA")

        if appdata:
            folders.append(
                Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            )

        if programdata:
            folders.append(
                Path(programdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            )

        return folders

    def _discover_shortcuts(self) -> list[Application]:
        apps: list[Application] = []

        for folder in self._start_menu_folders():
            if not folder.exists():
                continue

            for shortcut in folder.rglob("*.lnk"):
                apps.append(
                    Application(
                        name=shortcut.stem,
                        launch_target=str(shortcut),
                        launch_type="shortcut",
                        source="start_menu",
                    )
                )

        return apps

    def _discover_start_apps(self) -> list[Application]:
        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-StartApps | Select-Object Name,AppID | ConvertTo-Json -Compress",
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=12,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return []

        if result.returncode != 0 or not result.stdout.strip():
            return []

        try:
            raw = json.loads(result.stdout)
        except json.JSONDecodeError:
            return []

        if isinstance(raw, dict):
            raw = [raw]

        apps: list[Application] = []

        for item in raw:
            name = item.get("Name")
            app_id = item.get("AppID")

            if not name or not app_id:
                continue

            apps.append(
                Application(
                    name=name,
                    launch_target=app_id,
                    launch_type="app_id",
                    source="get_start_apps",
                )
            )

        return apps

    def refresh_applications(self) -> int:
        discovered = self._discover_shortcuts()
        discovered.extend(self._discover_start_apps())

        # Remove duplicate display-name/target combinations.
        unique: dict[tuple[str, str], Application] = {}
        for app in discovered:
            key = (
                self._normalise(app.name),
                self._normalise(app.launch_target),
            )
            unique[key] = app

        self._applications = list(unique.values())
        return len(self._applications)

    def find_application(self, query: str) -> Application | None:
        query_n = self._normalise(query)

        if not query_n:
            return None

        # Exact normalized name.
        for app in self._applications:
            if self._normalise(app.name) == query_n:
                return app

        # Prefer useful substring matches.
        substring_matches = [
            app
            for app in self._applications
            if query_n in self._normalise(app.name)
            or self._normalise(app.name) in query_n
        ]

        if substring_matches:
            return max(
                substring_matches,
                key=lambda app: SequenceMatcher(
                    None,
                    query_n,
                    self._normalise(app.name),
                ).ratio(),
            )

        # Fuzzy fallback.
        scored = [
            (
                SequenceMatcher(
                    None,
                    query_n,
                    self._normalise(app.name),
                ).ratio(),
                app,
            )
            for app in self._applications
        ]

        if not scored:
            return None

        score, best = max(scored, key=lambda item: item[0])

        # Deliberately conservative: don't open Calculator because the user
        # vaguely asked for "calendar", for example.
        if score < 0.58:
            return None

        return best

    def _launch(self, app: Application) -> None:
        if app.launch_type == "shortcut":
            os.startfile(app.launch_target)  # Windows-only by design.
            return

        if app.launch_type == "app_id":
            # shell:AppsFolder supports UWP/Store apps and many registered
            # desktop applications, including apps that are not on PATH.
            subprocess.Popen(
                [
                    "explorer.exe",
                    f"shell:AppsFolder\\{app.launch_target}",
                ]
            )
            return

        raise RuntimeError(f"Unknown launch type: {app.launch_type}")

    def open_application(self, query: str) -> str:
        app = self.find_application(query)

        if app is None:
            # Refresh once in case an app was installed after JARVIS started.
            self.refresh_applications()
            app = self.find_application(query)

        if app is None:
            return f"I couldn't find an installed application matching '{query}', Sir."

        try:
            self._launch(app)
            return f"Opening {app.name}, Sir."
        except Exception as exc:
            return f"I found {app.name}, but Windows could not launch it: {exc}"
