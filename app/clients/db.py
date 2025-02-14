import contextlib
import logging
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_sessionmaker, create_async_engine)


class PostgresDB:

    def __init__(self, pg_url: str) -> None:
        self._engine = create_async_engine(url=pg_url)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self, autocommit: bool = True) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()
        try:
            yield session
            if autocommit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
