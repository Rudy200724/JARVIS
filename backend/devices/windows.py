from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from difflib import SequenceMatcher
from pathlib import Path

from devices.base import Application, Device

# Built-in Windows utilities that are always guaranteed to exist
BUILTIN_APPS: dict[str, dict[str, str]] = {
    "notepad": {
        "name": "Notepad",
        "target": "notepad.exe",
        "type": "command",
    },
    "calculator": {
        "name": "Calculator",
        "target": "calc.exe",
        "type": "command",
    },
    "command prompt": {
        "name": "Command Prompt",
        "target": "cmd.exe",
        "type": "command",
    },
    "windows powershell": {
        "name": "Windows PowerShell",
        "target": "powershell.exe",
        "type": "command",
    },
    "file explorer": {
        "name": "File Explorer",
        "target": "explorer.exe",
        "type": "command",
    },
    "task manager": {
        "name": "Task Manager",
        "target": "taskmgr.exe",
        "type": "command",
    },
    "control panel": {
        "name": "Control Panel",
        "target": "control.exe",
        "type": "command",
    },
    "paint": {
        "name": "Paint",
        "target": "mspaint.exe",
        "type": "command",
    },
    "settings": {
        "name": "Settings",
        "target": "ms-settings:",
        "type": "uri",
    },
    "snipping tool": {
        "name": "Snipping Tool",
        "target": "snippingtool.exe",
        "type": "command",
    },
}

# Common queries and aliases mapped to standard application targets / display names
ALIASES: dict[str, list[str]] = {
    "vscode": ["visual studio code", "code"],
    "vs code": ["visual studio code", "code"],
    "code": ["visual studio code"],
    "visual studio code": ["visual studio code", "code"],
    "chrome": ["google chrome"],
    "google chrome": ["google chrome"],
    "browser": ["google chrome", "microsoft edge", "firefox", "brave", "opera"],
    "web browser": ["google chrome", "microsoft edge", "firefox", "brave", "opera"],
    "internet": ["google chrome", "microsoft edge"],
    "edge": ["microsoft edge"],
    "ms edge": ["microsoft edge"],
    "msedge": ["microsoft edge"],
    "microsoft edge": ["microsoft edge"],
    "cmd": ["command prompt"],
    "cmd exe": ["command prompt"],
    "cmd prompt": ["command prompt"],
    "command prompt": ["command prompt"],
    "terminal": ["terminal", "windows terminal", "command prompt", "powershell"],
    "windows terminal": ["terminal", "windows terminal"],
    "powershell": ["windows powershell", "powershell"],
    "pwsh": ["windows powershell", "powershell"],
    "calc": ["calculator"],
    "calculator": ["calculator"],
    "notepad": ["notepad"],
    "note pad": ["notepad"],
    "explorer": ["file explorer"],
    "files": ["file explorer"],
    "file explorer": ["file explorer"],
    "my computer": ["file explorer"],
    "this pc": ["file explorer"],
    "task manager": ["task manager"],
    "taskmgr": ["task manager"],
    "settings": ["settings"],
    "windows settings": ["settings"],
    "control panel": ["control panel"],
    "paint": ["paint", "mspaint"],
    "mspaint": ["paint"],
    "spotify": ["spotify"],
    "discord": ["discord"],
    "steam": ["steam"],
    "whatsapp": ["whatsapp"],
    "word": ["word", "microsoft word"],
    "excel": ["excel", "microsoft excel"],
    "powerpoint": ["powerpoint", "microsoft powerpoint"],
    "ppt": ["powerpoint", "microsoft powerpoint"],
}

# Substrings that indicate documentation, uninstallers, or auxiliary helpers
JUNK_KEYWORDS = (
    "uninstall",
    "remove",
    "help",
    "documentation",
    "manual",
    "pydoc",
    "faq",
    "release notes",
    "readme",
    "about",
    "diagnostics",
    "license",
)


class WindowsDevice(Device):
    """
    Discovers and launches Windows applications on the local machine
    without hard-coding paths or manual configurations.

    Discovery sources:
      1. Built-in Windows core utilities (Notepad, Calculator, CMD, Explorer, etc.)
      2. User & System Start Menu shortcuts (.lnk, .url)
      3. Desktop shortcuts
      4. Windows Get-StartApps catalog (Store / UWP & desktop registered apps)
      5. Windows PATH executables fallback
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
        userprofile = os.environ.get("USERPROFILE")
        public = os.environ.get("PUBLIC")

        if appdata:
            folders.append(
                Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            )
            folders.append(
                Path(appdata) / "Microsoft" / "Windows" / "Start Menu"
            )

        if programdata:
            folders.append(
                Path(programdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            )
            folders.append(
                Path(programdata) / "Microsoft" / "Windows" / "Start Menu"
            )

        if userprofile:
            folders.append(Path(userprofile) / "Desktop")

        if public:
            folders.append(Path(public) / "Desktop")

        return folders

    def _discover_builtin_apps(self) -> list[Application]:
        apps: list[Application] = []
        for key, item in BUILTIN_APPS.items():
            apps.append(
                Application(
                    name=item["name"],
                    launch_target=item["target"],
                    launch_type=item["type"],
                    source="builtin",
                )
            )
        return apps

    def _discover_shortcuts(self) -> list[Application]:
        apps: list[Application] = []

        for folder in self._start_menu_folders():
            if not folder.exists():
                continue

            for ext in ("*.lnk", "*.url"):
                try:
                    for shortcut in folder.rglob(ext):
                        apps.append(
                            Application(
                                name=shortcut.stem,
                                launch_target=str(shortcut),
                                launch_type="shortcut",
                                source="start_menu",
                            )
                        )
                except Exception:
                    continue

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
                encoding="utf-8",
                errors="replace",
                timeout=12,
                check=False,
            )
        except Exception:
            return []

        if result.returncode != 0 or not result.stdout.strip():
            return []

        try:
            raw = json.loads(result.stdout)
        except Exception:
            return []

        if isinstance(raw, dict):
            raw = [raw]

        apps: list[Application] = []

        for item in raw:
            name = item.get("Name")
            app_id = item.get("AppID")

            if not name or not app_id:
                continue

            launch_type = "app_id"
            if app_id.startswith(("http://", "https://", "steam://")):
                launch_type = "uri"
            elif Path(app_id).suffix.lower() in {".exe", ".bat", ".cmd", ".msc"} and Path(app_id).exists():
                launch_type = "executable"

            apps.append(
                Application(
                    name=name,
                    launch_target=app_id,
                    launch_type=launch_type,
                    source="get_start_apps",
                )
            )

        return apps

    def refresh_applications(self) -> int:
        discovered: list[Application] = []
        # 1. Built-in core apps first
        discovered.extend(self._discover_builtin_apps())
        # 2. Start menu and desktop shortcuts
        discovered.extend(self._discover_shortcuts())
        # 3. Get-StartApps catalogue
        discovered.extend(self._discover_start_apps())

        # Remove duplicate display-name/target combinations.
        unique: dict[tuple[str, str], Application] = {}
        for app in discovered:
            key = (
                self._normalise(app.name),
                self._normalise(app.launch_target),
            )
            if key not in unique:
                unique[key] = app

        self._applications = list(unique.values())
        return len(self._applications)

    def get_applications(self) -> list[Application]:
        return list(self._applications)

    def _is_junk(self, name: str) -> bool:
        lowered = name.lower()
        return any(junk in lowered for junk in JUNK_KEYWORDS)

    def find_application(self, query: str) -> Application | None:
        query_clean = re.sub(r"^(the|a|an)\s+", "", query.strip(), flags=re.IGNORECASE)
        query_n = self._normalise(query_clean)

        if not query_n:
            return None

        # Build prioritized list of search targets: exact query first, then aliases
        candidate_terms = [query_n]
        if query_n in ALIASES:
            for alias in ALIASES[query_n]:
                alias_n = self._normalise(alias)
                if alias_n not in candidate_terms:
                    candidate_terms.append(alias_n)

        # 1. Check exact match across candidate terms
        for term in candidate_terms:
            matches = [
                app for app in self._applications
                if self._normalise(app.name) == term
            ]
            if matches:
                # Prioritize non-junk app
                clean_matches = [m for m in matches if not self._is_junk(m.name)]
                return clean_matches[0] if clean_matches else matches[0]

        # 2. Check whole-word matches (e.g. query "chrome" matching "Google Chrome")
        for term in candidate_terms:
            word_matches = [
                app for app in self._applications
                if term in self._normalise(app.name).split()
            ]
            if word_matches:
                clean_matches = [m for m in word_matches if not self._is_junk(m.name)]
                pool = clean_matches if clean_matches else word_matches
                return max(
                    pool,
                    key=lambda app: SequenceMatcher(
                        None, term, self._normalise(app.name)
                    ).ratio(),
                )

        # 3. Check substring matches
        for term in candidate_terms:
            sub_matches = [
                app for app in self._applications
                if (term in self._normalise(app.name) or self._normalise(app.name) in term)
            ]
            if sub_matches:
                clean_matches = [m for m in sub_matches if not self._is_junk(m.name)]
                pool = clean_matches if clean_matches else sub_matches
                return max(
                    pool,
                    key=lambda app: SequenceMatcher(
                        None, term, self._normalise(app.name)
                    ).ratio(),
                )

        # 4. Fuzzy fallback across all applications
        scored: list[tuple[float, Application]] = []
        for term in candidate_terms:
            for app in self._applications:
                norm_name = self._normalise(app.name)
                ratio = SequenceMatcher(None, term, norm_name).ratio()
                if self._is_junk(app.name):
                    ratio -= 0.3
                scored.append((ratio, app))

        if scored:
            score, best = max(scored, key=lambda item: item[0])
            if score >= 0.58:
                return best

        # 5. Check Windows PATH for executable
        target_path = shutil.which(query_n) or shutil.which(f"{query_n}.exe")
        if target_path:
            return Application(
                name=query_clean.title(),
                launch_target=target_path,
                launch_type="executable",
                source="path",
            )

        return None

    def _launch(self, app: Application) -> None:
        target = app.launch_target
        launch_type = app.launch_type

        # 1. URIs (http://, https://, steam://, ms-settings:, etc.)
        if launch_type == "uri" or (":" in target and not Path(target).is_absolute()):
            try:
                os.startfile(target)
                return
            except Exception:
                subprocess.Popen(["explorer.exe", target])
                return

        # 2. Shortcuts (.lnk, .url)
        if launch_type == "shortcut":
            try:
                os.startfile(target)
                return
            except Exception:
                subprocess.Popen(["explorer.exe", target])
                return

        # 3. Direct executable or file on disk
        if launch_type == "executable" or (os.path.isabs(target) and os.path.exists(target)):
            try:
                os.startfile(target)
                return
            except Exception:
                subprocess.Popen([target])
                return

        # 4. Standard command (e.g. calc.exe, notepad.exe, cmd.exe)
        if launch_type == "command":
            try:
                os.startfile(target)
                return
            except Exception:
                subprocess.Popen(target, shell=True)
                return

        # 5. UWP / AppID via Shell:AppsFolder
        if launch_type == "app_id":
            if target.startswith(("http://", "https://", "steam://")):
                os.startfile(target)
                return

            if os.path.exists(target):
                os.startfile(target)
                return

            apps_folder_target = f"shell:AppsFolder\\{target}"
            try:
                os.startfile(apps_folder_target)
                return
            except Exception:
                subprocess.Popen(["explorer.exe", apps_folder_target])
                return

        # Fallback for any other type
        try:
            os.startfile(target)
        except Exception:
            subprocess.Popen(target, shell=True)

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
