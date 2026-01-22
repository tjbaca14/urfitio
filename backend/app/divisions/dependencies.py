"""Division domain dependencies."""

from fastapi import Depends

from app.divisions.repository import DivisionRepository, division_repository
from app.divisions.service import DivisionService


async def get_division_repository() -> DivisionRepository:
    """Get DivisionRepository instance."""
    return division_repository


async def get_division_service(
    repository: DivisionRepository = Depends(get_division_repository),
) -> DivisionService:
    """Get DivisionService instance with repository."""
    return DivisionService(repository)
