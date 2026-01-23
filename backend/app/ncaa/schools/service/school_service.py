"""School service - business logic for schools."""

from typing import List, Optional

from app.ncaa.schools.models import SchoolResponse
from app.ncaa.schools.repository import SchoolRepository
from app.utils import EntityNotFoundError, get_logger
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def get_school_by_id(
        self,
        session: AsyncSession,
        school_id: str,
    ) -> SchoolResponse:
        """
        Get a school by ID.

        Args:
            session: Database session
            school_id: School ID

        Returns:
            SchoolResponse

        Raises:
            EntityNotFoundError: If school not found
        """
        school = await self.repository.get_by_id(session, school_id)

        if not school:
            raise EntityNotFoundError(f"School not found: {school_id}")

        return SchoolResponse.model_validate(school)

    async def list_schools(
        self,
        session: AsyncSession,
        division_id: Optional[str] = None,
        name_contains: Optional[str] = None,
        limit: Optional[int] = 100,
    ) -> List[SchoolResponse]:
        """
        List schools with optional filters.

        Args:
            session: Database session
            division_id: Optional filter by division ID
            name_contains: Filter by partial name match (currently ignored)
            limit: Maximum number of schools to return

        Returns:
            List of SchoolResponse objects

        Raises:
            EntityNotFoundError: If no schools found
        """
        # Build kwargs for filtering
        kwargs = {}
        if division_id:
            kwargs["division_id"] = division_id

        schools = await self.repository.get_all(
            session=session,
            limit=limit,
            **kwargs,
        )

        if not schools:
            if division_id:
                raise EntityNotFoundError(
                    f"No schools found in division '{division_id}'"
                )
            else:
                raise EntityNotFoundError("No schools found")

        return [SchoolResponse.model_validate(school) for school in schools]
