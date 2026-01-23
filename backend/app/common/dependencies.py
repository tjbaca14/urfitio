from typing import AsyncGenerator

from app.common.clients.http_client import HTTPClient
from app.integrations.llm.base import LLMProvider
from app.settings import LLMConfig
from fastapi import Request


async def get_http_client(request: Request) -> HTTPClient:
    return request.app.state.http_client


async def get_llm_config(request: Request) -> LLMConfig:
    return request.app.state.llm_config


async def get_llm_provider(request: Request) -> LLMProvider:
    """Get LLM provider instance (Anthropic, OpenAI, etc.)."""
    return request.app.state.llm_provider


async def get_db_session(request: Request) -> AsyncGenerator[AsyncGenerator, None]:
    async with request.app.state.db.session() as session:
        yield session
