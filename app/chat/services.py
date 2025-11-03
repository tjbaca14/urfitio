from datetime import datetime
from typing import List, Optional

import pytz
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.models.api import ChatRequest
from app.chat.models.dto import (ChatHistoryCreateDTO, ChatHistoryDTO,
                                 ChatHistoryUpdateDTO)
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
        created_date = chat_request.createdDate or datetime.now(
            pytz.timezone("America/Los_Angeles")
        )
        updated_date = datetime.now(pytz.timezone("America/Los_Angeles"))

        # Create DTO
        chat_dto = ChatHistoryCreateDTO(
            id=chat_request.id,
            user_id=chat_request.userId,
            messages=messages,
            created_date=created_date,
        )

        # Save or update (upsert)
        saved_chat = await self.chat_repo.save_or_update_chat(
            session, chat_dto, updated_date=updated_date
        )

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
        chat = await self.chat_repo.get_chat_by_id(session, chat_id)

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
        chat_repo = ChatRepository()
        conversations = await chat_repo.get_user_chats(
            session, user_id, limit=limit, offset=offset
        )
        logger.debug(f"Retrieved {len(conversations)} conversations for user {user_id}")
        return conversations

    async def get_recent_conversations(
        self, session: AsyncSession, user_id: str, days: int = 7, limit: int = 10
    ) -> List[ChatHistoryDTO]:
        """
        Get recent conversations for a user.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID
            days: Number of days to look back
            limit: Maximum number of conversations to return

        Returns:
            List of recent ChatHistoryDTO
        """

        conversations = await self.chat_repo.get_recent_user_chats(
            session, user_id, days=days, limit=limit
        )
        logger.debug(
            f"Retrieved {len(conversations)} recent conversations for user {user_id}"
        )
        return conversations

    async def append_message(
        self, session: AsyncSession, chat_id: str, message: Message
    ) -> Optional[ChatHistoryDTO]:
        """
        Append a new message to an existing conversation.

        Args:
            session: SQLAlchemy async session
            chat_id: Chat identifier
            message: Message to append

        Returns:
            Updated ChatHistoryDTO or None if chat not found
        """

        # Get existing chat
        chat = await self.chat_repo.get_chat_by_id(session, chat_id)
        if not chat:
            logger.warning(f"Cannot append message: chat not found {chat_id}")
            return None

        # Append new message
        updated_messages = chat.messages + [message.model_dump()]
        updated_date = datetime.now(pytz.timezone("America/Los_Angeles"))

        update_dto = ChatHistoryUpdateDTO(
            messages=updated_messages, updated_date=updated_date
        )

        updated_chat = await self.chat_repo.update_chat_messages(
            session, chat_id, update_dto
        )

        if updated_chat:
            logger.info(f"Message appended to conversation {chat_id}")

        return updated_chat

    async def delete_conversation(self, session: AsyncSession, chat_id: str) -> bool:
        """
        Delete a conversation.

        Args:
            session: SQLAlchemy async session
            chat_id: Chat identifier

        Returns:
            True if deleted, False if not found
        """
        deleted = await self.chat_repo.delete_chat(session, chat_id)
        return deleted

    async def delete_user_conversations(
        self, session: AsyncSession, user_id: str
    ) -> int:
        """
        Delete all conversations for a user.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID

        Returns:
            Number of conversations deleted
        """
        count = await self.chat_repo.delete_user_chats(session, user_id)
        logger.info(f"Deleted {count} conversations for user {user_id}")
        return count
