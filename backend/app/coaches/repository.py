from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.coaches.models import DivisionDTO, SchoolDTO
from app.common.db_model import Coach, Division, School
from app.common.repository import BaseRepository


class CoachRepository(BaseRepository[Coach]):
    """
    Repository for CoachIndex entity.
    Handles coach data storage and retrieval.
    """

    def __init__(self):
        super().__init__(Coach)

    async def get_all_divisions(
        self, session: AsyncSession
    ) -> Optional[List[DivisionDTO]]:
        """
        Get all divisions from the division table.

        Args:
            session: SQLAlchemy async session

        Returns:
            List of Division entities with id and division_type
        """
        query = select(Division)
        result = await session.execute(query)
        rows = result.scalars().all()
        if not rows:
            return None

        return [DivisionDTO.model_validate(row) for row in rows]

    async def get_school_by_id(
        self, session: AsyncSession, school_id: str
    ) -> Optional[SchoolDTO]:
        """
        Get a school by its ID.

        Args:
            session: SQLAlchemy async session
            school_id: School identifier

        Returns:
            School entity or None
        """
        query = select(School).where(School.id == school_id)
        result = await session.execute(query)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return SchoolDTO.model_validate(row)

    async def get_school_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[SchoolDTO]:
        """
        Get a school by its exact name.

        Args:
            session: SQLAlchemy async session
            name: School name

        Returns:
            School entity or None
        """
        query = select(School).where(School.name == name)
        result = await session.execute(query)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return SchoolDTO.model_validate(row)

    async def list_schools(
        self,
        session: AsyncSession,
        division_id: Optional[str] = None,
        name_contains: Optional[str] = None,
        limit: Optional[int] = 100,
    ) -> Optional[List[SchoolDTO]]:
        """
        List schools with optional filtering.

        Args:
            session: SQLAlchemy async session
            division_id: Filter by division ID (e.g., "d1")
            name_contains: Filter by partial name match (case-insensitive)
            limit: Maximum number of schools to return

        Returns:
            List of School entities
        """
        query = select(School)

        # Apply filters
        if division_id:
            query = query.where(School.division_id == division_id)

        if name_contains:
            query = query.where(School.name.ilike(f"%{name_contains}%"))

        # Apply limit
        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        rows = result.scalars().all()
        if not rows:
            return None
        return [SchoolDTO.model_validate(row) for row in rows]
