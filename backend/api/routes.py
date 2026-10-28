from api.auth import get_current_user

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from api.schemas import ChatRequest, ChatResponse
from core.assistant import Assistant
from tools.applications import open_application, refresh_applications, list_applications

router = APIRouter()

assistant = Assistant()


class AppActionRequest(BaseModel):
    app_name: str


@router.post("/chat")
async def chat(request: ChatRequest, user: str = Depends(get_current_user)):
    return StreamingResponse(
        assistant.stream_response(request.message),
        media_type="text/plain"
    )


@router.post("/applications/open")
def open_app(request: AppActionRequest, user: str = Depends(get_current_user)):
    message = open_application(request.app_name)
    return {"status": "ok", "message": message}


@router.post("/applications/refresh")
def refresh_apps(user: str = Depends(get_current_user)):
    message = refresh_applications()
    return {"status": "ok", "message": message}
