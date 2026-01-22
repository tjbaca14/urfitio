"""Division service - business logic for divisions."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.divisions.models import DivisionResponse
from app.divisions.repository import DivisionRepository
from app.utils import EntityNotFoundError, get_logger

logger = get_logger(__name__)


class DivisionService:
    """
    Service for division business logic.

    Responsibilities:
    - Domain queries for divisions
    - Business logic for division data
    """

    def __init__(self, repository: DivisionRepository) -> None:
        """
        Initialize division service.

        Args:
            repository: Repository for database access
        """
        self.repository = repository

    async def get_all_divisions(self, session: AsyncSession) -> List[DivisionResponse]:
        """
        Get all available NCAA divisions.

        Args:
            session: Database session

        Returns:
            List of division response objects

        Raises:
            EntityNotFoundError: If no divisions exist
        """
        divisions = await self.repository.get_all(session)

        if not divisions:
            raise EntityNotFoundError("No divisions found")

        return [DivisionResponse.model_validate(div) for div in divisions]

    async def get_division_by_id(
        self, session: AsyncSession, division_id: str
    ) -> DivisionResponse:
        """
        Get a division by ID.

        Args:
            session: Database session
            division_id: Division identifier

        Returns:
            Division response object

        Raises:
            EntityNotFoundError: If division not found
        """
        division = await self.repository.get_by_id(session, division_id)

        if not division:
            raise EntityNotFoundError(f"Division not found: {division_id}")

        return DivisionResponse.model_validate(division)
