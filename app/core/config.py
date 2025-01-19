from datetime import timedelta

from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    URL: str
    API_KEY: str
    MAX_TOKENS: int
    MODEL: str
    TEMPERATURE: float


class PostgresSettings(BaseSettings):
    database: str
    host: str
    username: str
    password: str
    port: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class AuthenticatinSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int
    SIGNUP_TOKEN_EXPIRE: int

    @property
    def access_token_expire_minutes(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE)

    @property
    def refresh_token_expire_days(self) -> timedelta:
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE)

    @property
    def signup_token_expire_minutes(self) -> timedelta:
        return timedelta(days=self.SIGNUP_TOKEN_EXPIRE)


class EmailSettings(BaseSettings):
    source_email: str
    source_domain: str
    SMTP_SERVER: str
    SMTP_PORT: int # TLS
    SMTP_USERNAME: str
    SMTP_PASSWORD:  str


llm_config = LLMConfig()  # type: ignore

auth_settings = AuthenticatinSettings()  # type: ignore

postgres_settings = PostgresSettings()  # type: ignore

email_settings = EmailSettings()
