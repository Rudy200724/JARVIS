from api.auth import get_current_user

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from api.schemas import ChatRequest, ChatResponse
from core.assistant import Assistant

router=APIRouter()

assistant=Assistant()

@router.post("/chat")
async def chat(request:ChatRequest, user: str = Depends(get_current_user)):

    return StreamingResponse(
        assistant.stream_response(request.message),
        media_type="text/plain"
    )
