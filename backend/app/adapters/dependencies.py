"""Dependencies for adapter layer."""

from fastapi import Depends

from app.adapters.school_retriever import SchoolContextRetriever
from app.common.dependencies import get_school_cache_service
from app.rag.pipeline import Retriever
from app.schools.service.cache_service import SchoolCacheService


async def get_retriever(
    school_cache_service: SchoolCacheService = Depends(get_school_cache_service),
) -> Retriever:
    """
    Get context retriever implementation.

    This is where we wire up the concrete adapter (SchoolContextRetriever)
    to the generic Retriever protocol. Other domains depend on Retriever,
    not on the concrete implementation.

    Args:
        school_cache_service: School cache service from app state

    Returns:
        Retriever implementation (currently SchoolContextRetriever)
    """
    return SchoolContextRetriever(school_cache_service)
