from pydantic import BaseModel, ConfigDict


class BaseDTOModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    """
    Universal message format for LLM conversations.

    Used across domains:
    - Chat domain (ChatRequest)
    - LLM integrations (provider APIs)
    - RAG pipeline (message flow)

    This is a shared primitive, not domain-specific.
    """

    role: str
    content: str
