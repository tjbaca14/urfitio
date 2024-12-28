from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    URL: str
    API_KEY: str
    MAX_TOKENS: int
    MODEL: str
    TEMPERATURE: float


llm_config = LLMConfig()
