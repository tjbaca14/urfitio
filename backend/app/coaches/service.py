from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.coaches.models import DivisionResponse, SchoolResponse
from app.coaches.repository import CoachRepository
from app.utils import EntityNotFoundError, get_logger

logger = get_logger(__name__)


class CoachService:
    """
    Pure domain service for coach and school business logic.

    Responsibilities:
    - Domain queries for UI/API (divisions, schools)
    - Business logic for school and coach data
    """

    def __init__(self, repository: CoachRepository) -> None:
        """
        Initialize coach service.

        Args:
            repository: Repository for database access
        """
        self.repository = repository

    async def get_divisions(self, session: AsyncSession) -> List[DivisionResponse]:
        """
        Domain query: Get all available NCAA divisions.

        Args:
            session: Database session

        Returns:
            List of division objects with id and division_type
        """
        divisions = await self.repository.get_all_divisions(session)
        if not divisions:
            raise EntityNotFoundError("No divisions")
        return [DivisionResponse.model_validate(div) for div in divisions]

    async def get_school_by_id(
        self, session: AsyncSession, school_id: str
    ) -> SchoolResponse:
        """
        Get a school by ID or name.

        Args:
            session: Database session
            school_id: School ID or name

        Returns:
            SchoolDTO or None if not found
        """
        school = await self.repository.get_school_by_id(session, school_id)

        if not school:
            raise EntityNotFoundError(f"No school with id: {school_id}")

        return SchoolResponse.model_validate(school)

    async def list_schools(
        self,
        session: AsyncSession,
        division: Optional[str] = None,
        name_contains: Optional[str] = None,
        limit: Optional[int] = 100,
    ) -> List[SchoolResponse]:
        """
        List schools with optional filtering.

        Args:
            session: Database session
            division: Filter by division ID (e.g., "d1")
            name_contains: Filter by partial name match
            limit: Maximum number of schools to return

        Returns:
            List of SchoolDTO objects
        """
        schools = await self.repository.list_schools(
            session=session,
            division_id=division,
            name_contains=name_contains,
            limit=limit,
        )
        if not schools:
            raise EntityNotFoundError(f"No schools for division with id: {division}")
        return [SchoolResponse.model_validate(school) for school in schools]
