from fastapi import Depends, APIRouter


from app.dependencies import get_claude_api, get_cache
from app.models.chat import ChatRequest, Message
from app.services.claude_service import ClaudeAPI
from app.util import get_logger
from app.services.rag_service import rag_service
from typing import Dict

logger = get_logger(__name__)

chat_router = APIRouter(prefix="/api/v1", tags=["Chat"])

@chat_router.post("/chat", response_model=Message)
async def chat_endpoint(
    chat_request: ChatRequest,
    cache: Dict[str,str] = Depends(get_cache),
    claude_api: ClaudeAPI = Depends(get_claude_api),
) -> Message:
    logger.info(f"Input messages: {chat_request}")
    resp = await rag_service(cache=cache, chat_request=chat_request, claude_api=claude_api)
    return resp