"""Division repository - data access for Division entities."""

from app.common.repository import BaseRepository
from app.ncaa.db_models import Division
from app.ncaa.divisions.models import DivisionDTO


class DivisionRepository(BaseRepository[Division, DivisionDTO]):
    """
    Repository for Division entity.
    Handles division data storage and retrieval.
    Returns DivisionDTO instances instead of ORM models.
    """

    def __init__(self):
        super().__init__(Division, DivisionDTO)


division_repository = DivisionRepository()
