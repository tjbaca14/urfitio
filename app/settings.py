from dataclasses import dataclass
from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    URL: str
    API_KEY: str
    MAX_TOKENS: int
    MODEL: str
    TEMPERATURE: float
    PROVIDER: str = "anthropic"


class DBSettings(BaseSettings):
    DATABASE: str
    HOST: str
    USER: str
    PASSWORD: str
    PORT: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


@dataclass
class AppSettings:
    llm_config: LLMConfig
    db_settings: DBSettings


def create_app_settings() -> AppSettings:
    return AppSettings(
        llm_config=LLMConfig(), # type: ignore
        db_settings=DBSettings(), # type: ignore
    )