"""
School context retriever for RAG.

Implements the Retriever protocol using NCAA school domain services.
"""

from typing import Optional

from app.ncaa.schools.service.cache_service import SchoolCacheService
from app.utils import get_logger

logger = get_logger(__name__)


class SchoolContextRetriever:
    """
    Retrieves school-specific context for RAG.

    This retriever allows RAG pipelines to retrieve school context
    without having direct knowledge of school domain internals.
    """

    def __init__(self, cache_service: SchoolCacheService):
        """
        Initialize school context retriever.

        Args:
            cache_service: School cache service for retrieving contexts
        """
        self._cache_service = cache_service

    async def retrieve(self, query: str) -> Optional[str]:
        """
        Retrieve school context based on school name query.

        Implements the Retriever protocol required by RAGPipeline.

        Args:
            query: School name to look up

        Returns:
            School context if found, None otherwise
        """
        context = await self._cache_service.get_school_context(query)

        if context:
            logger.info(f"Retrieved context for school: {query}")
        else:
            logger.warning(f"No context found for school: {query}")

        return context
