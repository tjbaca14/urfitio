"""School repository - data access for School entities."""

from app.common.db_model import School
from app.common.repository import BaseRepository
from app.schools.models import SchoolDTO


class SchoolRepository(BaseRepository[School, SchoolDTO]):
    """
    Repository for School entity.
    Inherits all CRUD operations from BaseRepository with support for filtering.
    Returns SchoolDTO instances instead of ORM models.
    """

    def __init__(self):
        super().__init__(School, SchoolDTO)


school_repository = SchoolRepository()
