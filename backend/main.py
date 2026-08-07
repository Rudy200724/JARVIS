from core.assistant import Assistant
from fastapi import FastAPI


app=FastAPI()

assistant=Assistant()

@app.get("/")
def root():
    return {"message": "JARVIS Backend Running"}

@app.post("/chat")
def chat(request):

    reply=assistant.chat(request.message)

    return {"response":reply}