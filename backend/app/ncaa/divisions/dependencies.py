"""Division dependencies."""

from app.ncaa.divisions.repository import (DivisionRepository,
                                           division_repository)
from app.ncaa.divisions.service import DivisionService
from fastapi import Depends


async def get_division_repository() -> DivisionRepository:
    """Get DivisionRepository instance."""
    return division_repository


async def get_division_service(
    repository: DivisionRepository = Depends(get_division_repository),
) -> DivisionService:
    """Get DivisionService instance with repository."""
    return DivisionService(repository)
