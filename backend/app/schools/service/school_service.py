"""School service - business logic for schools."""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.schools.models import SchoolResponse
from app.schools.repository import SchoolRepository
from app.utils import EntityNotFoundError, get_logger

logger = get_logger(__name__)


class SchoolService:
    """
    Service for school business logic.

    Responsibilities:
    - Domain queries for schools
    - Business logic for school data
    """

    def __init__(self, repository: SchoolRepository) -> None:
        """
        Initialize school service.

        Args:
            repository: Repository for database access
        """
        self.repository = repository

    async def get_school_in_division(
        self,
        session: AsyncSession,
        division_id: str,
        school_id: str,
    ) -> SchoolResponse:
        """
        Get a school by ID within a specific division.

        Uses generic BaseRepository filtering with division_id as a kwarg
        to ensure the school belongs to the specified division.

        Args:
            session: Database session
            division_id: Division ID (e.g., "d1")
            school_id: School ID

        Returns:
            SchoolResponse

        Raises:
            EntityNotFoundError: If school not found in division
        """
        # Use base repository method with division_id filter
        school = await self.repository.get_by_id(
            session, school_id, division_id=division_id
        )

        if not school:
            raise EntityNotFoundError(
                f"School '{school_id}' not found in division '{division_id}'"
            )

        return SchoolResponse.model_validate(school)

    async def list_schools_in_division(
        self,
        session: AsyncSession,
        division_id: str,
        name_contains: Optional[str] = None,
        limit: Optional[int] = 100,
    ) -> List[SchoolResponse]:
        """
        List schools within a specific division.

        Uses generic BaseRepository filtering with division_id as a kwarg.
        Note: name_contains filtering is not yet supported by BaseRepository.

        Args:
            session: Database session
            division_id: Division ID (required, e.g., "d1")
            name_contains: Filter by partial name match (currently ignored)
            limit: Maximum number of schools to return

        Returns:
            List of SchoolResponse objects

        Raises:
            EntityNotFoundError: If no schools found in division
        """

        schools = await self.repository.get_all(
            session=session,
            division_id=division_id,
            limit=limit,
        )

        if not schools:
            raise EntityNotFoundError(f"No schools found in division '{division_id}'")

        return [SchoolResponse.model_validate(school) for school in schools]
