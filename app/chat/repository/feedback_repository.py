from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.db_model import Feedback
from ..models.dto import FeedbackCreateDTO, FeedbackDTO
from app.common.repository import BaseRepository


class FeedbackRepository(BaseRepository[Feedback]):
    """
    Repository for Feedback entity.
    Handles user feedback storage and retrieval.
    """

    def __init__(self):
        super().__init__(Feedback)

    async def get_feedback_by_id(
        self, session: AsyncSession, feedback_id: str
    ) -> Optional[FeedbackDTO]:
        """
        Get feedback by ID.

        Args:
            session: SQLAlchemy async session
            feedback_id: Feedback identifier

        Returns:
            FeedbackDTO or None
        """
        feedback = await self.get_by_id(session, feedback_id, "id")
        return FeedbackDTO.model_validate(feedback) if feedback else None

    async def get_user_feedback(
        self,
        session: AsyncSession,
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[FeedbackDTO]:
        """
        Get all feedback submitted by a specific user.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID
            limit: Maximum number of feedback records to return
            offset: Number of records to skip

        Returns:
            List of FeedbackDTO
        """
        query = (
            select(Feedback)
            .where(Feedback.user_id == user_id)
            .order_by(Feedback.created_date.desc())
            .offset(offset)
        )

        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        feedbacks = result.scalars().all()
        return [FeedbackDTO.model_validate(fb) for fb in feedbacks]

    async def get_feedback_by_category(
        self,
        session: AsyncSession,
        category: str,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[FeedbackDTO]:
        """
        Get feedback filtered by category.

        Args:
            session: SQLAlchemy async session
            category: Feedback category
            limit: Maximum number of feedback records to return
            offset: Number of records to skip

        Returns:
            List of FeedbackDTO
        """
        query = (
            select(Feedback)
            .where(Feedback.category == category)
            .order_by(Feedback.created_date.desc())
            .offset(offset)
        )

        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        feedbacks = result.scalars().all()
        return [FeedbackDTO.model_validate(fb) for fb in feedbacks]

    async def create_feedback(
        self, session: AsyncSession, feedback_dto: FeedbackCreateDTO
    ) -> FeedbackDTO:
        """
        Create a new feedback record.

        Args:
            session: SQLAlchemy async session
            feedback_dto: Feedback creation data

        Returns:
            Created FeedbackDTO
        """
        feedback = Feedback(
            id=feedback_dto.id,
            user_id=feedback_dto.user_id,
            feedback=feedback_dto.feedback,
            category=feedback_dto.category,
            created_date=feedback_dto.created_date,
        )
        created_feedback = await self.create(session, feedback)
        return FeedbackDTO.model_validate(created_feedback)

    async def delete_feedback(self, session: AsyncSession, feedback_id: str) -> bool:
        """
        Delete feedback by ID.

        Args:
            session: SQLAlchemy async session
            feedback_id: Feedback identifier

        Returns:
            True if deleted, False if not found
        """
        return await self.delete(session, feedback_id, "id")

    async def delete_user_feedback(self, session: AsyncSession, user_id: str) -> int:
        """
        Delete all feedback for a user.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID

        Returns:
            Number of feedback records deleted
        """
        query = select(Feedback).where(Feedback.user_id == user_id)
        result = await session.execute(query)
        feedbacks = result.scalars().all()

        count = 0
        for feedback in feedbacks:
            await session.delete(feedback)
            count += 1

        await session.flush()
        return count

    async def get_all_feedback(
        self, session: AsyncSession, limit: Optional[int] = None, offset: int = 0
    ) -> List[FeedbackDTO]:
        """
        Get all feedback with optional pagination.

        Args:
            session: SQLAlchemy async session
            limit: Maximum number of feedback records to return
            offset: Number of records to skip

        Returns:
            List of FeedbackDTO
        """
        feedbacks = await self.get_all(session, limit=limit, offset=offset)
        return [FeedbackDTO.model_validate(fb) for fb in feedbacks]
