"""Chat routes - API endpoints for chat operations."""

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.dependencies import get_conversation_service, get_rag_pipeline
from app.chat.models.dto import ChatHistoryDTO, ChatRequest
from app.chat.services import ConversationService
from app.common.dependencies import get_db_session
from app.common.models import Message
from app.rag.pipeline import RAGPipeline
from app.utils import get_logger

logger = get_logger(__name__)

chat_router = APIRouter(
    prefix="/api/v1/chats",
    tags=["Chat API"],
)


@chat_router.post("", response_model=Message)
async def post_chat(
    chat_request: ChatRequest,
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> Message:
    """
    Process a chat request with RAG (Retrieval-Augmented Generation).

    Flow:
    1. Retrieve context based on contextQuery (if provided)
    2. Augment messages with context
    3. Call LLM to generate response
    4. Return assistant's message

    Args:
        chat_request: Chat request with messages and optional context query

    Returns:
        Assistant's response message
    """
    logger.info(f"Chat request received: {chat_request.id}")

    response_message = await rag_pipeline.generate(
        messages=chat_request.messages,
        context_query=chat_request.context_query,
    )

    logger.info(f"Response generated for chat {chat_request.id}")
    return response_message


@chat_router.put("/{chat_id}", response_model=ChatRequest)
async def save_chat(
    chat_id: str = Path(..., description="Chat identifier"),
    chat_request: ChatRequest = Body(...),
    conversation_service: ConversationService = Depends(get_conversation_service),
    session: AsyncSession = Depends(get_db_session),
) -> ChatRequest:
    """
    Save/update a chat conversation (upsert).

    Args:
        chat_id: Chat identifier (from URL path)
        chat_request: Chat conversation with messages
        conversation_service: Service for chat persistence
        session: Database session

    Returns:
        Saved chat conversation

    Raises:
        400: If path chat_id doesn't match body id
    """
    # Ensure path ID matches body ID
    if chat_request.id != chat_id:
        raise HTTPException(status_code=400, detail="Path chat_id must match body id")

    logger.info(f"Saving chat: {chat_id}")
    await conversation_service.save_conversation(session, chat_request)

    return chat_request


@chat_router.get("/{chat_id}", response_model=ChatHistoryDTO)
async def get_chat(
    chat_id: str = Path(..., description="Chat identifier"),
    conversation_service: ConversationService = Depends(get_conversation_service),
    session: AsyncSession = Depends(get_db_session),
) -> ChatHistoryDTO:
    """
    Get chat history by ID.

    Args:
        chat_id: Chat identifier
        conversation_service: Service for chat retrieval
        session: Database session

    Returns:
        Chat history

    Raises:
        404: If chat not found
    """
    logger.info(f"Retrieving chat: {chat_id}")

    chat = await conversation_service.get_conversation(session, chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail=f"Chat not found: {chat_id}")

    return chat


@chat_router.get("/user/{user_id}", response_model=list[ChatHistoryDTO])
async def get_user_chats(
    user_id: str = Path(..., description="User identifier"),
    limit: int = 10,
    offset: int = 0,
    conversation_service: ConversationService = Depends(get_conversation_service),
    session: AsyncSession = Depends(get_db_session),
) -> list[ChatHistoryDTO]:
    """
    Get all chats for a user.

    Args:
        user_id: User identifier
        limit: Maximum number of chats to return
        offset: Number of chats to skip
        conversation_service: Service for chat retrieval
        session: Database session

    Returns:
        List of chat histories
    """
    logger.info(f"Retrieving chats for user: {user_id}")

    chats = await conversation_service.get_user_conversations(
        session, user_id, limit=limit, offset=offset
    )

    return chats
