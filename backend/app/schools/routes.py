"""School routes - API endpoints for schools (nested under divisions)."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dependencies import get_db_session
from app.schools.dependencies import get_school_service
from app.schools.models import SchoolResponse
from app.schools.service.school_service import SchoolService
from app.utils import EntityNotFoundError, get_logger

logger = get_logger(__name__)

schools_router = APIRouter(
    prefix="/api/v1/divisions/{division_id}/schools", tags=["Schools"]
)


@schools_router.get("/{school_id}")
async def get_school_in_division(
    division_id: str = Path(..., description="Division ID (e.g., 'd1')"),
    school_id: str = Path(..., description="School ID"),
    service: SchoolService = Depends(get_school_service),
    session: AsyncSession = Depends(get_db_session),
) -> SchoolResponse:
    """
    Get a single school within a division.

    Validates that the division exists and that the school belongs to that division.

    Args:
        division_id: Division identifier (e.g., 'd1', 'd2', 'd3')
        school_id: School identifier

    Returns:
        School resource

    Raises:
        404: Division not found or school not found in division

    Example:
        GET /api/v1/divisions/d1/schools/stanford

        Response:
        {
            "id": "stanford",
            "name": "Stanford",
            "division_id": "d1",
            "context": "..."
        }
    """
    try:
        school = await service.get_school_in_division(session, division_id, school_id)
        return school
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@schools_router.get("")
async def list_schools_in_division(
    division_id: str = Path(..., description="Division ID (e.g., 'd1')"),
    name_contains: Optional[str] = Query(None, description="Search by partial name"),
    limit: Optional[int] = Query(100, description="Max results", ge=1, le=500),
    service: SchoolService = Depends(get_school_service),
    session: AsyncSession = Depends(get_db_session),
) -> List[SchoolResponse]:
    """
    List schools within a specific division.

    Validates that the division exists before listing schools.

    Path parameters:
    - division_id: Division identifier (required)

    Query parameters:
    - name_contains: Partial name search (case-insensitive)
    - limit: Maximum results (default: 100)

    Examples:
    - GET /api/v1/divisions/d1/schools                     → All D1 schools
    - GET /api/v1/divisions/d1/schools?name_contains=State → D1 schools with "State"
    - GET /api/v1/divisions/d1/schools?limit=10            → First 10 D1 schools

    Returns:
        List of school resources

    Raises:
        404: Division not found or no schools in division
    """
    try:
        schools = await service.list_schools_in_division(
            session=session,
            division_id=division_id,
            name_contains=name_contains,
            limit=limit,
        )
        return schools
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
