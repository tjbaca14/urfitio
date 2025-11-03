from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.models.api import ChatRequest
from app.chat.orchestrator import ChatOrchestrator
from app.common.models import Message
from app.chat.dependencies import get_chat_orchestrator
from app.common.dependencies import get_db_session
from app.utils import get_logger

logger = get_logger(__name__)

chat_router = APIRouter(
    prefix="/api/v1",
    tags=["Chat API"],
)


@chat_router.post("/chat", response_model=Message)
async def post_chat(
    chat_request: ChatRequest,
    orchestrator: ChatOrchestrator = Depends(get_chat_orchestrator),
) -> Message:
    """
    Process a chat request with RAG (Retrieval-Augmented Generation).

    Flow:
    1. Retrieve context based on contextQuery (if provided)
    2. Augment messages with context
    3. Call LLM to generate response
    4. Return assistant's message

    The RAG pipeline (retrieve→augment→generate) is handled by the orchestrator.
    """
    logger.info(f"Chat request received: {chat_request.id}")
    response_message = await orchestrator.process_chat(chat_request)
    return response_message


@chat_router.post("/save/chat", response_model=ChatRequest)
async def save_chat(
    chat_request: ChatRequest,
    orchestrator: ChatOrchestrator = Depends(get_chat_orchestrator),
    db_session: AsyncSession = Depends(get_db_session),
) -> ChatRequest:
    """
    Save a chat conversation to the database.

    Args:
        chat_request: Chat conversation with messages
    """
    logger.info(f"Saving chat: {chat_request.id}")
    await orchestrator.save_chat(db_session, chat_request)
    return chat_request
