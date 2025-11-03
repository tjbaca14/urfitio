from fastapi import Depends

from app.chat.orchestrator import ChatOrchestrator, create_chat_orchestrator
from app.common.dependencies import get_cache, get_llm_provider
from app.integrations.llm import BaseLLMProvider


async def get_chat_orchestrator(
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
    cache: dict = Depends(get_cache),
) -> ChatOrchestrator:
    return create_chat_orchestrator(cache, llm_provider)
