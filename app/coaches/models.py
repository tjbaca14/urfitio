from typing import Optional

from pydantic import BaseModel, ConfigDict


# Response models
class DivisionDTO(BaseModel):
    """Division resource representation."""

    model_config = ConfigDict(from_attributes=True)
    id: str
    division_type: str


class DivisionResponse(DivisionDTO):
    pass


class SchoolDTO(BaseModel):
    """School resource representation."""

    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    division_id: str
    context: Optional[str] = None


class SchoolResponse(SchoolDTO):
    pass
