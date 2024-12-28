from pydantic import BaseModel

class School(BaseModel):
    id: str
    name: str