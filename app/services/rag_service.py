from typing import Dict

from app.models.chat import ChatRequest, Message
from app.services.claude_service import ClaudeAPI


async def rag_service(
    cache: Dict[str, str], chat_request: ChatRequest, claude_api: ClaudeAPI
) -> Message:
    # retrieve context
    messages = chat_request.messages
    context = cache.get(chat_request.contextKey)
    # pass context into school name
    user_query = f"User query: {chat_request.messages[-1]}"
    message_context = f"Context: {context}\n\n"
    messages[-1].content = message_context + user_query
    resp = await claude_api.generate(messages)
    return resp
