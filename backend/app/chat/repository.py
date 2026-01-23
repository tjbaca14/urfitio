"""Chat repository - data access for chat history."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from app.chat.models.db_models import ChatHistory
from app.chat.models.dto import ChatHistoryDTO
from app.common.repository import BaseRepository
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository(BaseRepository[ChatHistory, ChatHistoryDTO]):
    """
    Repository for ChatHistory entity.
    Handles chat conversation storage and retrieval.
    Returns ChatHistoryDTO instances instead of ORM models.
    """

    def __init__(self):
        super().__init__(ChatHistory, ChatHistoryDTO)

    async def get_user_chats(
        self,
        session: AsyncSession,
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[ChatHistoryDTO]:
        """
        Get all chats for a specific user, ordered by most recent.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID
            limit: Maximum number of chats to return
            offset: Number of records to skip

        Returns:
            List of ChatHistoryDTO
        """
        query = (
            select(ChatHistory)
            .where(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.created_date.desc())
            .offset(offset)
        )

        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        chats = result.scalars().all()
        return [self._orm_to_dto(chat) for chat in chats]

    async def save_or_update_chat(
        self, session: AsyncSession, chat_history_dto: ChatHistoryDTO
    ) -> ChatHistoryDTO:
        """
        Save new chat or update existing chat (upsert operation).

        Args:
            session: SQLAlchemy async session
            chat_history_dto: Chat history DTO to save/update

        Returns:
            Saved/Updated ChatHistoryDTO
        """
        return await self.update(session, chat_history_dto)

    async def update_chat_messages(
        self,
        session: AsyncSession,
        chat_id: str,
        messages: List[dict],
        updated_date: datetime,
    ) -> Optional[ChatHistoryDTO]:
        """
        Update messages in existing chat.

        Args:
            session: SQLAlchemy async session
            chat_id: Chat identifier
            messages: Updated messages list
            updated_date: Update timestamp

        Returns:
            Updated ChatHistoryDTO or None if not found
        """
        query = (
            update(ChatHistory)
            .where(ChatHistory.id == chat_id)
            .values(messages=messages, updated_date=updated_date)
            .returning(ChatHistory)
        )
        result = await session.execute(query)
        updated_chat = result.scalars().first()
        await session.flush()

        return self._orm_to_dto(updated_chat) if updated_chat else None

    async def get_recent_user_chats(
        self, session: AsyncSession, user_id: str, days: int = 7, limit: int = 10
    ) -> List[ChatHistoryDTO]:
        """
        Get recent chats for a user within specified days.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID
            days: Number of days to look back
            limit: Maximum number of chats to return

        Returns:
            List of recent ChatHistoryDTO
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        query = (
            select(ChatHistory)
            .where(
                ChatHistory.user_id == user_id,
                ChatHistory.created_date >= cutoff_date,
            )
            .order_by(ChatHistory.created_date.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        chats = result.scalars().all()
        return [self.dto.model_validate(chat) for chat in chats]

    async def delete_user_chats(self, session: AsyncSession, user_id: str) -> int:
        """
        Delete all chats for a user.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID

        Returns:
            Number of chats deleted
        """
        query = select(ChatHistory).where(ChatHistory.user_id == user_id)
        result = await session.execute(query)
        chats = result.scalars().all()

        count = 0
        for chat in chats:
            await session.delete(chat)
            count += 1

        await session.flush()
        return count
