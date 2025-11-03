


from fastapi import Depends
from app.coaches.service import CoachService
from app.common.dependencies import get_cache


async def get_coach_service(cache: dict = Depends(get_cache)) -> CoachService:
    return CoachService(cache)
