"""School domain models."""

from typing import Optional

from app.common.models import BaseDTOModel


class SchoolDTO(BaseDTOModel):
    """School data transfer object."""

    id: str
    name: str
    division_id: str
    context: Optional[str] = None


class SchoolResponse(BaseDTOModel):
    """School API response model."""

    id: str
    name: str
    division_id: str
    context: Optional[str] = None
