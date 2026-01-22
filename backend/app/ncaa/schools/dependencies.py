"""School dependencies."""

from fastapi import Depends, Request

from app.common.clients.cache import CacheClient
from app.ncaa.schools.repository import SchoolRepository, school_repository
from app.ncaa.schools.service.cache_service import SchoolCacheService
from app.ncaa.schools.service.school_service import SchoolService


async def get_school_repository() -> SchoolRepository:
    """Get SchoolRepository instance."""
    return school_repository


async def get_school_service(
    repository: SchoolRepository = Depends(get_school_repository),
) -> SchoolService:
    """Get SchoolService instance with repository."""
    return SchoolService(repository)


async def get_cache_client(request: Request) -> CacheClient:
    """Get cache client from application state."""
    return request.app.state.cache_client


async def get_school_cache_service(request: Request) -> SchoolCacheService:
    """
    Get school cache service from application state.

    This is used by the chat domain to retrieve school context for RAG.
    """
    return request.app.state.school_cache_service
