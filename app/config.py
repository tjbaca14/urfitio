from pydantic_settings import BaseSettings


class ClaudeConfig(BaseSettings):
    URL: str
    API_KEY: str
    MAX_TOKENS: int
    MODEL: str
    TEMPERATURE: float


claude_config = ClaudeConfig()
