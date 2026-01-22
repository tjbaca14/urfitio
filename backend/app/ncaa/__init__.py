"""NCAA domain - divisions and schools data."""

from .divisions.routes import divisions_router
from .schools.routes import schools_router

__all__ = ["divisions_router", "schools_router"]
