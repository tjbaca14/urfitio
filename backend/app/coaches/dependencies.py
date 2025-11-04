from app.coaches.repository import CoachRepository
from app.coaches.service import CoachService


def get_coach_service() -> CoachService:
    """Get CoachService instance with repository."""
    repository = CoachRepository()
    return CoachService(repository)
