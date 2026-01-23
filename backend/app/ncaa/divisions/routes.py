"""Division routes - API endpoints for divisions."""

from typing import List

from app.common.dependencies import get_db_session
from app.ncaa.divisions.dependencies import get_division_service
from app.ncaa.divisions.models import DivisionResponse
from app.ncaa.divisions.service import DivisionService
from app.utils import EntityNotFoundError, get_logger
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)

divisions_router = APIRouter(prefix="/api/v1/divisions", tags=["Divisions"])


@divisions_router.get("")
async def list_divisions(
    service: DivisionService = Depends(get_division_service),
    session: AsyncSession = Depends(get_db_session),
) -> List[DivisionResponse]:
    """
    Get all available NCAA divisions.

    Returns:
        List of division objects with id and division_type

    Example:
        GET /api/v1/divisions

        Response:
        [
            {"id": "d1", "division_type": "Division I"},
            {"id": "d2", "division_type": "Division II"},
            {"id": "d3", "division_type": "Division III"}
        ]
    """
    try:
        logger.info("Fetching all divisions")
        divisions = await service.get_all_divisions(session)
        return divisions
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@divisions_router.get("/{division_id}")
async def get_division(
    division_id: str = Path(..., description="Division ID (e.g., 'd1', 'd2')"),
    service: DivisionService = Depends(get_division_service),
    session: AsyncSession = Depends(get_db_session),
) -> DivisionResponse:
    """
    Get a single division by ID.

    Args:
        division_id: Division identifier (e.g., 'd1', 'd2', 'd3')

    Returns:
        Division object

    Raises:
        404: Division not found

    Example:
        GET /api/v1/divisions/d1

        Response:
        {"id": "d1", "division_type": "Division I"}
    """
    try:
        logger.info(f"Fetching division: {division_id}")
        division = await service.get_division_by_id(session, division_id)
        return division
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
