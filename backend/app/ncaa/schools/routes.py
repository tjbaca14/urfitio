"""School routes - API endpoints for schools."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dependencies import get_db_session
from app.ncaa.schools.dependencies import get_school_service
from app.ncaa.schools.models import SchoolResponse
from app.ncaa.schools.service.school_service import SchoolService
from app.utils import EntityNotFoundError, get_logger

logger = get_logger(__name__)

schools_router = APIRouter(prefix="/api/v1/schools", tags=["Schools"])


@schools_router.get("/{school_id}")
async def get_school(
    school_id: str = Path(..., description="School ID"),
    service: SchoolService = Depends(get_school_service),
    session: AsyncSession = Depends(get_db_session),
) -> SchoolResponse:
    """
    Get a single school by ID.

    Args:
        school_id: School identifier

    Returns:
        School resource

    Raises:
        404: School not found

    Example:
        GET /api/v1/schools/stanford

        Response:
        {
            "id": "stanford",
            "name": "Stanford",
            "division_id": "d1",
            "context": "..."
        }
    """
    try:
        school = await service.get_school_by_id(session, school_id)
        return school
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@schools_router.get("")
async def list_schools(
    division_id: Optional[str] = Query(
        None, description="Filter by division ID (e.g., 'd1')"
    ),
    name_contains: Optional[str] = Query(None, description="Search by partial name"),
    limit: Optional[int] = Query(100, description="Max results", ge=1, le=500),
    service: SchoolService = Depends(get_school_service),
    session: AsyncSession = Depends(get_db_session),
) -> List[SchoolResponse]:
    """
    List schools with optional filters.

    Query parameters:
    - division_id: Filter by division (optional)
    - name_contains: Partial name search (case-insensitive)
    - limit: Maximum results (default: 100)

    Examples:
    - GET /api/v1/schools                              → All schools
    - GET /api/v1/schools?division_id=d1               → All D1 schools
    - GET /api/v1/schools?name_contains=State          → Schools with "State" in name
    - GET /api/v1/schools?division_id=d1&limit=10      → First 10 D1 schools

    Returns:
        List of school resources

    Raises:
        404: No schools found matching filters
    """
    try:
        schools = await service.list_schools(
            session=session,
            division_id=division_id,
            name_contains=name_contains,
            limit=limit,
        )
        return schools
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
