
from typing import AsyncGenerator
from app.common.clients.http_client import HTTPClient
from app.integrations.llm.base import BaseLLMProvider
from app.integrations.llm.factory import LLMProviderFactory
from app.settings import LLMConfig
from fastapi import Request, Depends

async def get_http_client(request: Request) -> HTTPClient:
    return request.app.state.http_client

async def get_llm_config(request: Request) -> LLMConfig:
    return request.app.state.llm_config

async def get_llm_provider(
    http_client: HTTPClient = Depends(get_http_client),
    llm_config: LLMConfig = Depends(get_llm_config),
) -> BaseLLMProvider:
    """Get LLM provider instance (Anthropic, OpenAI, etc.)."""
    return LLMProviderFactory.create(
        config=llm_config,
        http_client=http_client,
    )

async def get_db_session(request: Request) -> AsyncGenerator[AsyncGenerator, None]:
    async with request.app.state.db.session() as session:
        yield session

async def get_cache(request: Request) -> dict:
    return request.app.state.cache