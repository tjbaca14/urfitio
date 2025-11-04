from pydantic import BaseModel


class Message(BaseModel):
    """
    Universal message format for LLM conversations.

    Used across domains:
    - Chat domain (ChatRequest/ChatResponse)
    - LLM integrations (provider APIs)
    - RAG pipeline (message flow)

    This is a shared primitive, not domain-specific.
    """

    role: str
    content: str
