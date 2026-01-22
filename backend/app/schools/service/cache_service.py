"""School cache service - builds school context cache."""

from typing import Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.clients.cache import CacheClient
from app.schools.models import SchoolDTO
from app.schools.repository import SchoolRepository
from app.utils import get_logger

logger = get_logger(__name__)


class SchoolCacheService:
    """
    Service for building school context cache.

    Responsible for populating cache with school data from database.
    """

    def __init__(self, repository: SchoolRepository, cache_client: CacheClient):
        """
        Initialize cache service.

        Args:
            repository: School repository for data access
            cache_client: Cache client for storage
        """
        self._repository = repository
        self._cache_client = cache_client

    async def build_cache(self, session: AsyncSession) -> None:
        """
        Build school context cache from database.

        Fetches all schools from database and populates the cache with
        school name -> context mappings.

        Args:
            session: Database session
        """
        logger.info("Building school context cache...")
        schools: List[SchoolDTO] = await self._repository.get_all(session, limit=None)

        if not schools:
            logger.warning("No schools found in database")
            return

        # Build cache entries: school name -> school context
        cache_items: Dict[str, str] = {
            school.name: school.context for school in schools if school.context
        }

        # Populate cache client
        await self._cache_client.set_many(cache_items)

        logger.info(f"School context cache built with {len(cache_items)} entries")

    async def refresh_cache(self, session: AsyncSession) -> None:
        """
        Refresh the cache by clearing and rebuilding from database.

        Args:
            session: Database session
        """
        logger.info("Refreshing school context cache...")
        await self._cache_client.clear()
        await self.build_cache(session)

    async def get_school_context(self, school_name: str) -> Optional[str]:
        """
        Get context for a specific school.

        Args:
            school_name: Name of the school

        Returns:
            School context if found, None otherwise
        """
        return await self._cache_client.get(school_name)

    async def get_all_contexts(self) -> Dict[str, str]:
        """
        Get all school contexts.

        Returns:
            Dict mapping school names to contexts
        """
        return await self._cache_client.get_all()
