from typing import Optional

import httpx

from app.common.clients.cache import (CacheClient, CacheClientType,
                                      create_cache_client)
from app.common.clients.db import PostgresDB
from app.common.clients.http_client import HTTPClient
from app.integrations.llm import BaseLLMProvider, LLMProviderFactory
from app.schools.repository import school_repository
from app.schools.service.cache_service import SchoolCacheService
from app.settings import AppSettings, create_app_settings
from app.utils import get_logger

logger = get_logger(__name__)


class ApplicationContainer:
    """
    DI container holding application-scoped clients.

    Initialized during FastAPI lifespan.
    """

    def __init__(self):
        """Initialize container with optional clients."""
        # Cache infrastructure (initialized during async _init_cache())
        self.cache_client: Optional[CacheClient] = None
        self.school_cache_service: Optional[SchoolCacheService] = None

        # Other clients (initialized during async initialize())
        self.httpx_client: Optional[httpx.AsyncClient] = None
        self.http_client: Optional[HTTPClient] = None
        self.db: Optional[PostgresDB] = None
        self.llm_provider: Optional[BaseLLMProvider] = None

    async def _init_cache(self) -> None:
        """
        Initialize cache infrastructure and build school context cache.

        Creates the cache client and school cache service, then populates
        the cache from the database. Access to cached data is through
        school_cache_service methods.
        """
        if not self.db:
            raise RuntimeError("DB instance not created")

        # Initialize cache infrastructure
        self.cache_client = create_cache_client(CacheClientType.IN_MEMORY)
        self.school_cache_service = SchoolCacheService(
            repository=school_repository,
            cache_client=self.cache_client,
        )

        async with self.db.session() as session:
            await self.school_cache_service.build_cache(session)

    async def initialize(self) -> "ApplicationContainer":
        """Initialize all application clients."""
        logger.info("Initializing application container...")
        app_settings: AppSettings = create_app_settings()

        # HTTP client
        self.httpx_client = httpx.AsyncClient()
        self.http_client = HTTPClient(
            client=self.httpx_client,
            logger=get_logger("http_client"),
        )

        # Database
        self.db = PostgresDB(pg_url=app_settings.db_settings.url)

        # LLM Provider
        self.llm_provider = LLMProviderFactory.create(
            config=app_settings.llm_config,
            http_client=self.http_client,
        )

        # Build caches
        await self._init_cache()

        logger.info("Application container initialized")
        return self

    async def close(self) -> None:
        """Clean up resources."""
        logger.info("Closing application container...")
        if self.httpx_client:
            await self.httpx_client.aclose()
        if self.db:
            await self.db.close()

        logger.info("Application container closed")
