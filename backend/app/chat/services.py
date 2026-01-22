from datetime import datetime
from typing import List, Optional

import pytz
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.models.dto import ChatHistoryDTO, ChatRequest
from app.common.models import Message
from app.utils import get_logger

from .repository import ChatRepository

logger = get_logger(__name__)


class ConversationService:
    """
    Service responsible for managing chat conversation persistence.
    Handles saving, retrieving, and updating chat history.
    """

    def __init__(self, chat_repo: ChatRepository) -> None:
        self.chat_repo = chat_repo

    async def save_conversation(
        self, session: AsyncSession, chat_request: ChatRequest
    ) -> ChatHistoryDTO:
        """
        Save or update a conversation.

        Args:
            session: SQLAlchemy async session
            chat_request: Chat request containing messages and metadata

        Returns:
            Saved ChatHistoryDTO
        """

        # Convert Message objects to dicts
        messages = [message.model_dump() for message in chat_request.messages]

        # Use provided created_date or current time
        created_date = chat_request.created_date or datetime.now(
            pytz.timezone("America/Los_Angeles")
        )
        updated_date = datetime.now(pytz.timezone("America/Los_Angeles"))

        # Create DTO
        chat_dto = ChatHistoryDTO(
            id=chat_request.id,
            user_id=chat_request.user_id,
            messages=messages,
            created_date=created_date,
            updated_date=updated_date,
        )

        # Save or update (upsert)
        saved_chat = await self.chat_repo.update(session, chat_dto)

        logger.info(
            f"Conversation saved: {saved_chat.id} for user {saved_chat.user_id}"
        )
        return saved_chat

    async def get_conversation(
        self, session: AsyncSession, chat_id: str
    ) -> Optional[ChatHistoryDTO]:
        """
        Get a conversation by ID.

        Args:
            session: SQLAlchemy async session
            chat_id: Chat identifier

        Returns:
            ChatHistoryDTO or None
        """
        chat = await self.chat_repo.get_by_id(session, chat_id)

        if chat:
            logger.debug(f"Conversation retrieved: {chat_id}")
        else:
            logger.warning(f"Conversation not found: {chat_id}")
        return chat

    async def get_user_conversations(
        self, session: AsyncSession, user_id: str, limit: int = 10, offset: int = 0
    ) -> List[ChatHistoryDTO]:
        """
        Get all conversations for a user.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID
            limit: Maximum number of conversations to return
            offset: Number of records to skip

        Returns:
            List of ChatHistoryDTO
        """
        conversations = await self.chat_repo.get_user_chats(
            session, user_id, limit=limit, offset=offset
        )
        logger.debug(f"Retrieved {len(conversations)} conversations for user {user_id}")
        return conversations
