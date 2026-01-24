"""Chat routes - API endpoints for school recruiting chat."""

from app.chat.dependencies import get_chat_application_service
from app.chat.models.dto import ChatHistoryDTO, ChatRequest
from app.chat.services.chat_application import ChatApplicationService
from app.common.dependencies import get_db_session
from app.common.models import Message
from app.utils import get_logger
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)

chat_router = APIRouter(
    prefix="/api/v1/chats",
    tags=["Chat API"],
)


@chat_router.post("", response_model=Message)
async def post_chat(
    chat_request: ChatRequest,
    chat_application_service: ChatApplicationService = Depends(
        get_chat_application_service
    ),
) -> Message:
    """
    Process a chat request with RAG (Retrieval-Augmented Generation).

    Flow:
    1. Retrieve context based on contextKey (if provided)
    2. Augment messages with context
    3. Call LLM to generate response
    4. Return assistant's message

    Args:
        chat_request: Chat request with messages and optional context query

    Returns:
        Assistant's response message
    """
    logger.info(f"Chat request received: {chat_request.id}")

    response_message = await chat_application_service.generate_response(chat_request)

    logger.info(f"Response generated for chat {chat_request.id}")
    return response_message


@chat_router.post("/{chat_id}", response_model=ChatRequest)
async def save_chat(
    chat_id: str = Path(..., description="Chat identifier"),
    chat_request: ChatRequest = Body(...),
    chat_application_service: ChatApplicationService = Depends(
        get_chat_application_service
    ),
    session: AsyncSession = Depends(get_db_session),
) -> ChatRequest:
    """
    Save/update a chat conversation (upsert).

    Args:
        chat_id: Chat identifier (from URL path)
        chat_request: Chat conversation with messages
        chat_application_service: Service for chat operations
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
    await chat_application_service.save_conversation(session, chat_request)

    return chat_request


@chat_router.get("/{chat_id}", response_model=ChatHistoryDTO)
async def get_chat(
    chat_id: str = Path(..., description="Chat identifier"),
    chat_application_service: ChatApplicationService = Depends(
        get_chat_application_service
    ),
    session: AsyncSession = Depends(get_db_session),
) -> ChatHistoryDTO:
    """
    Get chat history by ID.

    Args:
        chat_id: Chat identifier
        chat_application_service: Service for chat operations
        session: Database session

    Returns:
        Chat history

    Raises:
        404: If chat not found
    """
    logger.info(f"Retrieving chat: {chat_id}")

    chat = await chat_application_service.get_conversation(session, chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail=f"Chat not found: {chat_id}")

    return chat


@chat_router.get("/user/{user_id}", response_model=list[ChatHistoryDTO])
async def get_user_chats(
    user_id: str = Path(..., description="User identifier"),
    limit: int = 10,
    offset: int = 0,
    chat_application_service: ChatApplicationService = Depends(
        get_chat_application_service
    ),
    session: AsyncSession = Depends(get_db_session),
) -> list[ChatHistoryDTO]:
    """
    Get all chats for a user.

    Args:
        user_id: User identifier
        limit: Maximum number of chats to return
        offset: Number of chats to skip
        chat_application_service: Service for chat operations
        session: Database session

    Returns:
        List of chat histories
    """
    logger.info(f"Retrieving chats for user: {user_id}")

    chats = await chat_application_service.get_user_conversations(
        session, user_id, limit=limit, offset=offset
    )

    return chats
