from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.db_model import CoachIndex
from .models import (
    CoachIndexCreateDTO,
    CoachIndexDTO,
    CoachIndexUpdateDTO,
)
from app.common.repository import BaseRepository


class CoachRepository(BaseRepository[CoachIndex]):
    """
    Repository for CoachIndex entity.
    Handles coach data storage and retrieval.
    """

    def __init__(self):
        super().__init__(CoachIndex)

    async def get_coach_by_id(
        self, session: AsyncSession, coach_id: str
    ) -> Optional[CoachIndexDTO]:
        """
        Get coach by ID.

        Args:
            session: SQLAlchemy async session
            coach_id: Coach identifier

        Returns:
            CoachIndexDTO or None
        """
        coach = await self.get_by_id(session, coach_id, "coach_id")
        return CoachIndexDTO.model_validate(coach) if coach else None

    async def get_coaches_by_division(
        self,
        session: AsyncSession,
        division: str,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[CoachIndexDTO]:
        """
        Get all coaches in a specific division.

        Args:
            session: SQLAlchemy async session
            division: Division name
            limit: Maximum number of coaches to return
            offset: Number of records to skip

        Returns:
            List of CoachIndexDTO
        """
        query = select(CoachIndex).where(CoachIndex.division == division).offset(offset)

        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        coaches = result.scalars().all()
        return [CoachIndexDTO.model_validate(coach) for coach in coaches]

    async def create_coach(
        self, session: AsyncSession, coach_dto: CoachIndexCreateDTO
    ) -> CoachIndexDTO:
        """
        Create a new coach index record.

        Args:
            session: SQLAlchemy async session
            coach_dto: Coach creation data

        Returns:
            Created CoachIndexDTO
        """
        coach = CoachIndex(
            coach_id=coach_dto.coach_id,
            division=coach_dto.division,
            data=coach_dto.data,
        )
        created_coach = await self.create(session, coach)
        return CoachIndexDTO.model_validate(created_coach)

    async def update_coach(
        self, session: AsyncSession, coach_id: str, update_dto: CoachIndexUpdateDTO
    ) -> Optional[CoachIndexDTO]:
        """
        Update coach data.

        Args:
            session: SQLAlchemy async session
            coach_id: Coach identifier
            update_dto: Fields to update

        Returns:
            Updated CoachIndexDTO or None if not found
        """
        update_values = update_dto.model_dump(exclude_none=True)

        if not update_values:
            return await self.get_coach_by_id(session, coach_id)

        query = (
            update(CoachIndex)
            .where(CoachIndex.coach_id == coach_id)
            .values(**update_values)
            .returning(CoachIndex)
        )
        result = await session.execute(query)
        updated_coach = result.scalars().first()
        await session.flush()

        return CoachIndexDTO.model_validate(updated_coach) if updated_coach else None

    async def save_or_update_coach(
        self, session: AsyncSession, coach_dto: CoachIndexCreateDTO
    ) -> CoachIndexDTO:
        """
        Save new coach or update existing coach (upsert operation).

        Args:
            session: SQLAlchemy async session
            coach_dto: Coach data

        Returns:
            Saved/Updated CoachIndexDTO
        """
        coach = CoachIndex(
            coach_id=coach_dto.coach_id,
            division=coach_dto.division,
            data=coach_dto.data,
        )
        merged_coach = await self.update(session, coach)
        return CoachIndexDTO.model_validate(merged_coach)

    async def delete_coach(self, session: AsyncSession, coach_id: str) -> bool:
        """
        Delete a coach by ID.

        Args:
            session: SQLAlchemy async session
            coach_id: Coach identifier

        Returns:
            True if deleted, False if not found
        """
        return await self.delete(session, coach_id, "coach_id")

    async def delete_coaches_by_division(
        self, session: AsyncSession, division: str
    ) -> int:
        """
        Delete all coaches in a division.

        Args:
            session: SQLAlchemy async session
            division: Division name

        Returns:
            Number of coaches deleted
        """
        query = select(CoachIndex).where(CoachIndex.division == division)
        result = await session.execute(query)
        coaches = result.scalars().all()

        count = 0
        for coach in coaches:
            await session.delete(coach)
            count += 1

        await session.flush()
        return count

    async def get_all_coaches(
        self, session: AsyncSession, limit: Optional[int] = None, offset: int = 0
    ) -> List[CoachIndexDTO]:
        """
        Get all coaches with optional pagination.

        Args:
            session: SQLAlchemy async session
            limit: Maximum number of coaches to return
            offset: Number of records to skip

        Returns:
            List of CoachIndexDTO
        """
        coaches = await self.get_all(session, limit=limit, offset=offset)
        return [CoachIndexDTO.model_validate(coach) for coach in coaches]

    async def get_all_divisions(self, session: AsyncSession) -> List[str]:
        """
        Get list of all unique divisions.

        Args:
            session: SQLAlchemy async session

        Returns:
            List of division names
        """
        query = select(CoachIndex.division).distinct()
        result = await session.execute(query)
        divisions = result.scalars().all()
        return [div for div in divisions if div is not None]
