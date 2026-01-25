"""Base repository providing generic CRUD operations with DTO conversion."""

from typing import Generic, List, Optional, Type, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

TModel = TypeVar("TModel")
TDTO = TypeVar("TDTO", bound=BaseModel)


class BaseRepository(Generic[TModel, TDTO]):
    """
    Base repository providing common CRUD operations for any SQLAlchemy model.

    Returns DTOs instead of ORM models to decouple domain from persistence layer.

    Usage:
        class SchoolRepository(BaseRepository[School, SchoolDTO]):
            def __init__(self):
                super().__init__(School, SchoolDTO)
    """

    def __init__(self, model: Type[TModel], dto: Type[TDTO]):
        """
        Initialize repository with model and DTO types.

        Args:
            model: SQLAlchemy ORM model class
            dto: Pydantic DTO class for serialization
        """
        self.model = model
        self.dto = dto

    def _dto_to_orm(self, dto: TDTO) -> TModel:
        """
        Convert DTO to ORM model instance.

        Args:
            dto: Pydantic DTO instance

        Returns:
            ORM model instance
        """
        return cast(TModel, self.model(**dto.model_dump(exclude_unset=True)))

    def _orm_to_dto(self, orm_model) -> TDTO:
        """
        Convert ORM model instance to DTO.

        Args:
            orm_model: SQLAlchemy ORM model instance

        Returns:
            Pydantic DTO instance
        """
        return cast(TDTO, self.dto.model_validate(orm_model))

    def _apply_filters(self, query, **filters):
        """
        Apply dynamic filters to a query based on kwargs.

        Args:
            query: SQLAlchemy query object
            **filters: Keyword arguments where key is attribute name and value is filter value

        Returns:
            Modified query with filters applied

        Example:
            query = select(School)
            query = self._apply_filters(query, division_id="d1", name="Stanford")
        """
        for attr_name, attr_value in filters.items():
            if hasattr(self.model, attr_name):
                filter_column = getattr(self.model, attr_name)
                query = query.where(filter_column == attr_value)
        return query

    async def get_by_id(
        self, session: AsyncSession, id_value: str, id_column: str = "id", **filters
    ) -> Optional[TDTO]:
        """
        Get a single entity by its primary key or specified column with optional filters.

        Args:
            session: SQLAlchemy async session
            id_value: The value to search for
            id_column: The column name to search (default: "id")
            **filters: Additional filters as keyword arguments (e.g., division_id="d1")

        Returns:
            DTO instance or None if not found

        Example:
            # Simple lookup
            school = await repository.get_by_id(session, "stanford")

            # With parent validation
            school = await repository.get_by_id(session, "stanford", division_id="d1")
        """
        column = getattr(self.model, id_column)
        query = select(self.model).where(column == id_value)
        query = self._apply_filters(query, **filters)
        result = await session.execute(query)
        orm_model = result.scalars().first()

        return self._orm_to_dto(orm_model) if orm_model else None

    async def get_all(
        self,
        session: AsyncSession,
        limit: Optional[int] = None,
        offset: int = 0,
        **filters
    ) -> List[TDTO]:
        """
        Get all entities with optional pagination and filters.

        Args:
            session: SQLAlchemy async session
            limit: Maximum number of records to return
            offset: Number of records to skip
            **filters: Additional filters as keyword arguments (e.g., division_id="d1")

        Returns:
            List of DTO instances

        Example:
            # All schools
            schools = await repository.get_all(session)

            # Schools in specific division
            schools = await repository.get_all(session, division_id="d1")
        """
        query = select(self.model).offset(offset)
        query = self._apply_filters(query, **filters)

        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        orm_models = result.scalars().all()

        return [self._orm_to_dto(model) for model in orm_models]

    async def create(self, session: AsyncSession, dto: TDTO) -> TDTO:
        """
        Create a new entity.

        Args:
            session: SQLAlchemy async session
            dto: DTO instance to create

        Returns:
            Created entity as DTO
        """
        entity = self._dto_to_orm(dto)
        session.add(entity)
        await session.flush()  # Flush to get generated IDs without committing
        await session.refresh(entity)  # Refresh to get DB defaults
        return self._orm_to_dto(entity)

    async def upsert(self, session: AsyncSession, dto: TDTO) -> TDTO:
        """
        Update an existing entity.

        Args:
            session: SQLAlchemy async session
            dto: DTO instance to update

        Returns:
            Updated entity as DTO
        """
        entity = self._dto_to_orm(dto)
        merged = await session.merge(entity)
        await session.flush()
        await session.refresh(merged)
        return self._orm_to_dto(merged)

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
        dto = await self.get_by_id(session, id_value, id_column)
        if dto:
            # Get the ORM model for deletion
            column = getattr(self.model, id_column)
            query = select(self.model).where(column == id_value)
            result = await session.execute(query)
            entity = result.scalars().first()
            if entity:
                await session.delete(entity)
                await session.flush()
                return True
        return False

    async def exists(
        self, session: AsyncSession, id_value: str, id_column: str = "id", **filters
    ) -> bool:
        """
        Check if an entity exists with optional filters.

        Args:
            session: SQLAlchemy async session
            id_value: The value to search for
            id_column: The column name to search (default: "id")
            **filters: Additional filters as keyword arguments

        Returns:
            True if exists, False otherwise

        Example:
            # Check if school exists
            exists = await repository.exists(session, "stanford")

            # Check if school exists in specific division
            exists = await repository.exists(session, "stanford", division_id="d1")
        """
        dto = await self.get_by_id(session, id_value, id_column, **filters)
        return dto is not None
