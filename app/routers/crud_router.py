from typing import List

from fastapi import APIRouter, Depends, Query, Response

from app.core.authentication import verify_or_refresh_factory
from app.dependencies import get_cache
from app.models.school import School
from app.services.cache_service import get_school_names
from app.utils import get_logger

logger = get_logger(__name__)

crud_router = APIRouter(prefix="/api/v1", tags=["CRUD"])


@crud_router.get(
    "/schools",
)
async def get_schools(
    response: Response,
    division: str = Query(...), cache: dict = Depends(get_cache),
    user: str = Depends(verify_or_refresh_factory(required_scopes=["user"])),
) -> List[School]:
    resp = await get_school_names(cache=cache, division=division)
    return resp
