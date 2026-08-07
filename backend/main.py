from api.routes import router
from fastapi import FastAPI

app=FastAPI(
    title="JARVIS API",
    description="Backend API for the JARVIS AI Assistant",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "JARVIS Backend Running"
    }

app.include_router(router)