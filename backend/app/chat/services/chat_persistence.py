"""Conversation service - persistence for chat history."""

from typing import List, Optional

from app.chat.models.dto import ChatHistoryDTO
from app.chat.repository import ChatRepository
from app.utils import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)


class  ChatPersistenceService:
    """
    Service responsible for managing chat conversation persistence.
    Handles saving, retrieving, and updating chat history.
    """

    def __init__(self, chat_repo: ChatRepository) -> None:
        self.chat_repo = chat_repo

    async def save_conversation(
        self, session: AsyncSession, chat_history_dto: ChatHistoryDTO
    ) -> ChatHistoryDTO:
        """
        Save or update a conversation.

        Args:
            session: SQLAlchemy async session
            chat_history_dto: Chat history DTO to persist

        Returns:
            Saved ChatHistoryDTO
        """
        # Save or update (upsert)
        saved_chat = await self.chat_repo.upsert(session, chat_history_dto)

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
