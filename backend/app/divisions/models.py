"""Division domain models."""

from app.common.models import BaseDTOModel


class DivisionDTO(BaseDTOModel):
    """Division data transfer object."""

    id: str
    division_type: str


class DivisionResponse(BaseDTOModel):
    """Division API response model."""

    id: str
    division_type: str
