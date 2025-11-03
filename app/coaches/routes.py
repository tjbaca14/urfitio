from typing import List

from fastapi import APIRouter, Depends, Query

from app.coaches.service import CoachService
from app.coaches.dependencies import get_coach_service
from app.utils import get_logger

logger = get_logger(__name__)

coach_router = APIRouter(prefix="/api/v1", tags=["Coaches"])


@coach_router.get("/divisions")
async def get_divisions(
    coach_service: CoachService = Depends(get_coach_service),
) -> List[str]:
    """
    Get all available NCAA divisions.

    Used by UI for division dropdown/selection.

    Returns:
        List of division names (e.g., ["D1", "D2", "D3"])
    """
    logger.info("Fetching divisions")
    divisions = coach_service.get_divisions()
    return divisions


@coach_router.get("/schools")
async def get_schools(
    division: str = Query(..., description="Division name (e.g., 'D1')"),
    coach_service: CoachService = Depends(get_coach_service),
) -> List[str]:
    """
    Get all schools in a specific division.

    Used by UI for school dropdown/selection after user picks a division.

    Args:
        division: Division name

    Returns:
        List of school names in that division
    """
    logger.info(f"Fetching schools for division: {division}")
    schools = coach_service.get_schools(division)
    return schools
