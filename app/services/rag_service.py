from typing import Dict

from app.models.chat import ChatRequest, Message
from app.services.llm_service import LLMApi


async def rag_service(
    cache: Dict[str, str], chat_request: ChatRequest, llm_api: LLMApi
) -> Message:
    # retrieve context
    messages = chat_request.messages
    context = cache.get(chat_request.contextKey)
    # pass context into school name
    user_query = f"User query: {chat_request.messages[-1]}"
    message_context = f"Context: {context}\n\n"
    messages[-1].content = message_context + user_query
    resp = await llm_api.generate(messages)
    return resp
