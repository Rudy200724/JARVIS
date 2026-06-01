import os 
from dotenv import load_dotenv

load_dotenv()

openrouter_key=os.getenv("OPENROUTER_KEY")
elevenlabs_key=os.getenv("ELEVENLABS_KEY")

MODELS=[
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
    "deepseek/deepseek-chat-v3-0324",
]

messages=[
            {
                "role": "system",
                "content": """
    You are JARVIS, Rudy's futuristic AI assistant.

    Refer to the user as "Sir" naturally and occasionally.

    Be intelligent, conversational, witty, and slightly sarcastic in a charming way.
    Keep responses short and concise.
    """
            }]

VOICE_ID="JBFqnCBsd6RMkjVDRZzb"