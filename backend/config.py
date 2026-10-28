import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env reliably from the backend directory regardless of working directory
backend_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=backend_dir / ".env")

openrouter_key = os.getenv("OPENROUTER_KEY")
elevenlabs_key = os.getenv("ELEVENLABS_KEY")

MAX_TOKENS = 1024

MODELS = [
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
    "deepseek/deepseek-chat-v3-0324",
]

messages = [
    {
        "role": "system",
        "content": """
    You are JARVIS, Rudy's futuristic AI assistant.

    Refer to the user as "Sir" naturally and occasionally.

    Be intelligent, conversational, witty, and slightly sarcastic in a charming way.
    Keep responses short and concise.
    """
    }
]

VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
