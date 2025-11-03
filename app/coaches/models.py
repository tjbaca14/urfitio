from typing import Optional

from pydantic import BaseModel, ConfigDict


class CoachIndexDTO(BaseModel):
    """DTO for CoachIndex entity"""

    model_config = ConfigDict(from_attributes=True)

    coach_id: str
    division: Optional[str] = None
    data: dict


class CoachIndexCreateDTO(BaseModel):
    """DTO for creating coach index"""

    coach_id: str
    division: Optional[str] = None
    data: dict


class CoachIndexUpdateDTO(BaseModel):
    """DTO for updating coach index"""

    division: Optional[str] = None
    data: Optional[dict] = None
