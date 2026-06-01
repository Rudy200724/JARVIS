from datetime import datetime
import subprocess
import os

def open_app(app):

    APPS={
        "chrome": "chrome",
        "browser": "chrome",
        "vscode": "code",
        "VS code": "code",
        "visual studio code": "code",
        "notepad": "notepad",
        "calculator": "calc",
        "calc": "calc",
        "cmd": "cmd",
        "spotify":"spotify",
        "vs code": "code",
        "note pad": "notepad"
    }

    apps=APPS.get(app)

    if not apps:
        return "I don't know that application, Sir."
    
    try:
        print(f"Opening {app}")
        subprocess.Popen(apps)
        return f"opening {app}, Sir."
    
    except Exception as e:
            result=os.system(f"start {apps}")
            if result==0:

                return f"opening {app}, Sir."
            
            return f"Failed to open {app} :{e}"

def execute_command(text):

    text=text.lower().strip()
    text = text.replace(".", "")

    if text.startswith("open "):

        app = text.replace("open ","",1).strip()
        return open_app(app)
    
    elif "what is the time" in text or "current time" in text:

        now = datetime.now()

        return now.strftime("Today is %A, %d %B %Y and the time is %I:%M %p, Sir.")

    return None