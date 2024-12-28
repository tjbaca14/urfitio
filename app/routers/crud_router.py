from fastapi import Depends, APIRouter

from app.dependencies import get_cache
from app.util import get_logger
from app.services.cache_service import get_school_names
from app.models.school import School
from typing import List

logger = get_logger(__name__)

crud_router = APIRouter(prefix="/api/v1", tags=["CRUD"])

@crud_router.get("/schools")
async def get_schools(
    cache: dict = Depends(get_cache)
) -> List[School]:
    resp = await get_school_names(cache=cache)
    return resp