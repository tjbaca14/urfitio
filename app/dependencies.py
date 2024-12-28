import httpx
from fastapi import Depends, Request

from app.core.config import LLMConfig, llm_config
from app.services.llm_service import LLMApi


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


async def get_llm_config() -> LLMConfig:
    return llm_config


async def get_cache(request: Request) -> dict:
    return request.app.state.cache


async def get_llm_api(
    http_client: httpx.AsyncClient = Depends(get_http_client),
    llm_config: LLMConfig = Depends(get_llm_config),
) -> LLMApi:
    return LLMApi(config=llm_config, http_client=http_client)
