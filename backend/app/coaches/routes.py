from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.coaches.dependencies import get_coach_service
from app.coaches.models import DivisionResponse, SchoolResponse
from app.coaches.service import CoachService
from app.common.dependencies import get_db_session
from app.utils import EntityNotFoundError, get_logger

logger = get_logger(__name__)


schools_router = APIRouter(prefix="/api/v1/schools", tags=["Schools"])


@schools_router.get("/divisions")
async def get_divisions(
    coach_service: CoachService = Depends(get_coach_service),
    db_session: AsyncSession = Depends(get_db_session),
) -> List[DivisionResponse]:
    """
    Get all available NCAA divisions.

    Returns:
        List of division objects with id and division_type
    """
    try:
        logger.info("Fetching divisions")
        divisions = await coach_service.get_divisions(db_session)
    except EntityNotFoundError as enf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(enf))
    return divisions


@schools_router.get("/{school_id}")
async def get_school(
    school_id: str = Path(..., description="School ID or name"),
    coach_service: CoachService = Depends(get_coach_service),
    db_session: AsyncSession = Depends(get_db_session),
) -> SchoolResponse:
    """
    Get a single school by ID or name.

    Args:
        school_id: School identifier or exact name

    Returns:
        School resource

    Raises:
        404: School not found
    """
    try:
        school = await coach_service.get_school_by_id(db_session, school_id)
        return school
    except EntityNotFoundError as enf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(enf))


@schools_router.get("")
async def list_schools(
    division: Optional[str] = Query(
        None, description="Filter by division (e.g., 'd1')"
    ),
    name_contains: Optional[str] = Query(None, description="Search by partial name"),
    limit: Optional[int] = Query(100, description="Max results", ge=1, le=500),
    coach_service: CoachService = Depends(get_coach_service),
    db_session: AsyncSession = Depends(get_db_session),
) -> List[SchoolResponse]:
    """
    List schools with optional filtering.

    Query parameters:
    - division: Filter by division (e.g., 'd1')
    - name_contains: Partial name search (case-insensitive)
    - limit: Maximum results (default: 100)

    Examples:
    - GET /schools                       → All schools (up to limit)
    - GET /schools?division=d1           → All D1 schools
    - GET /schools?name_contains=State   → Schools with "State" in name
    - GET /schools?division=d1&limit=10  → First 10 D1 schools

    Returns:
        List of school resources
    """
    try:
        schools = await coach_service.list_schools(
            session=db_session,
            division=division,
            name_contains=name_contains,
            limit=limit,
        )
        return schools
    except EntityNotFoundError as enf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(enf))
