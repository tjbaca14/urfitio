"""School domain dependencies."""

from fastapi import Depends

from app.schools.repository import SchoolRepository, school_repository
from app.schools.service.school_service import SchoolService


async def get_school_repository() -> SchoolRepository:
    """Get SchoolRepository instance."""
    return school_repository


async def get_school_service(
    repository: SchoolRepository = Depends(get_school_repository),
) -> SchoolService:
    """Get SchoolService instance with repository."""
    return SchoolService(repository)
