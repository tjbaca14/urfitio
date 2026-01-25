"""Chat repository - data access for chat history."""

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
