# JARVIS Backend Phase 1 — Generic Windows application control

This patch replaces the old hard-coded `APPS = {...}` dictionary with
platform-aware application discovery.

## Folder layout

Copy these files into `backend/`:

```text
backend/
├── devices/
│   ├── __init__.py
│   ├── base.py
│   ├── manager.py
│   └── windows.py
├── tools/
│   ├── __init__.py
│   ├── applications.py
│   └── system.py
└── test_apps.py
```

Empty `__init__.py` files are included.

## Test locally on Windows

From the backend directory:

```powershell
python test_apps.py
```

Try:
- Spotify
- Visual Studio Code
- Discord
- Calculator
- Chrome

The code scans the Start Menu and Windows `Get-StartApps` catalogue instead
of requiring one hard-coded launcher per app.

## Important cloud/backend limitation

If your FastAPI backend runs on Render, local Windows commands cannot directly
launch programs on your laptop. Code such as `subprocess.Popen()` always
executes on the computer/server running Python.

The production architecture therefore needs:

```text
Vercel frontend
      |
Render JARVIS API
      |
secure WebSocket/device channel
      |
JARVIS Windows companion agent
      |
Windows applications
```

Android will later implement the same Device interface through an Android
companion. iOS will require a more restricted companion/Shortcuts-style layer.

## Next phase

1. Structured tool-call schema
2. Tool registry / permissions
3. Intent router
4. Local Windows companion agent
5. Cloud-to-device WebSocket channel
6. Android device adapter
