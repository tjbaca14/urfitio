from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

TModel = TypeVar("TModel")


class BaseRepository(Generic[TModel]):
    """
    Base repository providing common CRUD operations for any SQLAlchemy model.

    Usage:
        class UserRepository(BaseRepository[User]):
            def __init__(self):
                super().__init__(User)
    """

    def __init__(self, model: Type[TModel]):
        self.model = model

    async def get_by_id(
        self, session: AsyncSession, id_value: str, id_column: str = "id"
    ) -> Optional[TModel]:
        """
        Get a single entity by its primary key or specified column.

        Args:
            session: SQLAlchemy async session
            id_value: The value to search for
            id_column: The column name to search (default: "id")

        Returns:
            Model instance or None if not found
        """
        column = getattr(self.model, id_column)
        query = select(self.model).where(column == id_value)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_all(
        self, session: AsyncSession, limit: Optional[int] = None, offset: int = 0
    ) -> List[TModel]:
        """
        Get all entities with optional pagination.

        Args:
            session: SQLAlchemy async session
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of model instances
        """
        query = select(self.model).offset(offset)
        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, entity: TModel) -> TModel:
        """
        Create a new entity.

        Args:
            session: SQLAlchemy async session
            entity: Model instance to create

        Returns:
            Created model instance
        """
        session.add(entity)
        await session.flush()  # Flush to get generated IDs without committing
        await session.refresh(entity)  # Refresh to get DB defaults
        return entity

    async def update(self, session: AsyncSession, entity: TModel) -> TModel:
        """
        Update an existing entity.

        Args:
            session: SQLAlchemy async session
            entity: Model instance to update

        Returns:
            Updated model instance
        """
        merged = await session.merge(entity)
        await session.flush()
        await session.refresh(merged)
        return merged

    async def delete(
        self, session: AsyncSession, id_value: str, id_column: str = "id"
    ) -> bool:
        """
        Delete an entity by ID.

        Args:
            session: SQLAlchemy async session
            id_value: The value to search for
            id_column: The column name to search (default: "id")

        Returns:
            True if deleted, False if not found
        """
        entity = await self.get_by_id(session, id_value, id_column)
        if entity:
            await session.delete(entity)
            await session.flush()
            return True
        return False

    async def exists(
        self, session: AsyncSession, id_value: str, id_column: str = "id"
    ) -> bool:
        """
        Check if an entity exists.

        Args:
            session: SQLAlchemy async session
            id_value: The value to search for
            id_column: The column name to search (default: "id")

        Returns:
            True if exists, False otherwise
        """
        entity = await self.get_by_id(session, id_value, id_column)
        return entity is not None
