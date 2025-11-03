from fastapi import Depends

from app.chat.orchestrator import create_chat_orchestrator, ChatOrchestrator
from app.common.dependencies import get_llm_provider, get_cache
from app.integrations.llm import BaseLLMProvider

async def get_chat_orchestrator(
        llm_provider: BaseLLMProvider = Depends(get_llm_provider),
        cache: dict = Depends(get_cache)
) -> ChatOrchestrator:
    return create_chat_orchestrator(cache, llm_provider)