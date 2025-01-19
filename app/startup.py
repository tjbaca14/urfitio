from app.clients.db import PostgresDB
from app.core.config import postgres_settings


def init_db() -> PostgresDB:
    return PostgresDB(pg_url=postgres_settings.url)
