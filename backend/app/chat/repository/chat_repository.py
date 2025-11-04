from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.db_model import ChatHistory
from app.common.repository import BaseRepository

from ..models.dto import (ChatHistoryCreateDTO, ChatHistoryDTO,
                          ChatHistoryUpdateDTO)


class ChatRepository(BaseRepository[ChatHistory]):
    """
    Repository for ChatHistory entity.
    Handles chat conversation storage and retrieval.
    """

    def __init__(self):
        super().__init__(ChatHistory)

    async def get_chat_by_id(
        self, session: AsyncSession, chat_id: str
    ) -> Optional[ChatHistoryDTO]:
        """
        Get chat history by chat ID.

        Args:
            session: SQLAlchemy async session
            chat_id: Unique chat identifier

        Returns:
            ChatHistoryDTO or None
        """
        chat = await self.get_by_id(session, chat_id, "id")
        return ChatHistoryDTO.model_validate(chat) if chat else None

    async def get_user_chats(
        self,
        session: AsyncSession,
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[ChatHistoryDTO]:
        """
        Get all chats for a specific user.

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
        return [ChatHistoryDTO.model_validate(chat) for chat in chats]

    async def create_chat(
        self, session: AsyncSession, chat_dto: ChatHistoryCreateDTO
    ) -> ChatHistoryDTO:
        """
        Create a new chat history record.

        Args:
            session: SQLAlchemy async session
            chat_dto: Chat creation data

        Returns:
            Created ChatHistoryDTO
        """
        chat = ChatHistory(
            id=chat_dto.id,
            user_id=chat_dto.user_id,
            messages=chat_dto.messages,
            created_date=chat_dto.created_date,
        )
        created_chat = await self.create(session, chat)
        return ChatHistoryDTO.model_validate(created_chat)

    async def save_or_update_chat(
        self,
        session: AsyncSession,
        chat_dto: ChatHistoryCreateDTO,
        updated_date: Optional[datetime] = None,
    ) -> ChatHistoryDTO:
        """
        Save new chat or update existing chat (upsert operation).
        Uses merge to handle both insert and update.

        Args:
            session: SQLAlchemy async session
            chat_dto: Chat data
            updated_date: Optional update timestamp

        Returns:
            Saved/Updated ChatHistoryDTO
        """
        chat = ChatHistory(
            id=chat_dto.id,
            user_id=chat_dto.user_id,
            messages=chat_dto.messages,
            created_date=chat_dto.created_date,
            updated_date=updated_date,
        )
        merged_chat = await self.update(session, chat)
        return ChatHistoryDTO.model_validate(merged_chat)

    async def update_chat_messages(
        self, session: AsyncSession, chat_id: str, chat_update_dto: ChatHistoryUpdateDTO
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
        chat_messages = chat_update_dto.messages
        updated_date = chat_update_dto.updated_date
        query = (
            update(ChatHistory)
            .where(ChatHistory.id == chat_id)
            .values(messages=chat_messages, updated_date=updated_date)
            .returning(ChatHistory)
        )
        result = await session.execute(query)
        updated_chat = result.scalars().first()
        await session.flush()

        return ChatHistoryDTO.model_validate(updated_chat) if updated_chat else None

    async def delete_chat(self, session: AsyncSession, chat_id: str) -> bool:
        """
        Delete a chat by ID.

        Args:
            session: SQLAlchemy async session
            chat_id: Chat identifier

        Returns:
            True if deleted, False if not found
        """
        return await self.delete(session, chat_id, "id")

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
        return [ChatHistoryDTO.model_validate(chat) for chat in chats]
