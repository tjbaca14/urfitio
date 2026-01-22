from typing import Dict, Optional

import httpx

from app.coaches.repository import CoachRepository
from app.common.cache_builder import build_school_context_cache
from app.common.clients.db import PostgresDB
from app.common.clients.http_client import HTTPClient
from app.integrations.llm import BaseLLMProvider, LLMProviderFactory
from app.settings import AppSettings, create_app_settings
from app.utils import get_logger

logger = get_logger(__name__)


class ApplicationContainer:
    """
    DI container holding application-scoped clients.

    Initialized during FastAPI lifespan.
    """

    def __init__(self):
        self.httpx_client: Optional[httpx.AsyncClient] = None
        self.http_client: Optional[HTTPClient] = None
        self.db: Optional[PostgresDB] = None
        self.cache: Optional[Dict[str, str]] = None
        self.llm_provider: Optional[BaseLLMProvider] = None

    async def _init_cache(self) -> Dict[str, str]:
        """Initialize school context cache from database."""
        coach_repo = CoachRepository()
        if not self.db:
            raise RuntimeError("DB instance not created")
        async with self.db.session() as session:
            return await build_school_context_cache(session, coach_repo)

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

        self.cache = await self._init_cache()

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
