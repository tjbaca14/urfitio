from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.coaches.repository import CoachRepository


async def build_school_context_cache(
    session: AsyncSession,
    coach_repo: CoachRepository,
    # <-- Inject, don't create
) -> Dict[str, str]:
    """
    Build in-memory cache of
      school names to coach contexts.

    Args:
        session: Database session
        coach_repo: Coach repository instance

    Returns:
        Dict mapping school names to contexts
    """
    schools = await coach_repo.list_schools(session, limit=None)

    if not schools:
        return {}

    # Build cache
    cache = {school.name: school.context for school in schools if school.context}
    return cache
