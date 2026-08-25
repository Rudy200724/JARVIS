from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.schemas import ChatRequest, ChatResponse
from core.assistant import Assistant

router=APIRouter()

assistant=Assistant()

@router.post("/chat")
def chat(request:ChatRequest):

    return StreamingResponse(
        assistant.stream_response(request.message),
        media_type="text/plain"
    )
