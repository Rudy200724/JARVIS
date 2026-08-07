from fastapi import APIRouter
from api.schemas import ChatRequest, ChatResponse
from core.assistant import Assistant

router=APIRouter()

assistant=Assistant()

@router.post("/chat",response_model=ChatResponse)
def chat(request:ChatRequest):

    reply=assistant.chat(request.message)

    return ChatResponse(response=reply)
