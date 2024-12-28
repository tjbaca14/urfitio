from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_cache
from app.models.school import School
from app.services.cache_service import get_school_names
from app.util import get_logger

logger = get_logger(__name__)

crud_router = APIRouter(prefix="/api/v1", tags=["CRUD"])


@crud_router.get("/schools")
async def get_schools(cache: dict = Depends(get_cache)) -> List[School]:
    resp = await get_school_names(cache=cache)
    return resp
