from typing import Dict, List

from app.utils import get_logger

logger = get_logger(__name__)


class CoachService:
    """
    Pure domain service for coach business logic.

    Responsibilities:
    - Domain queries for UI/API (divisions, schools)
    - Direct coach data accessLe

    The cache structure is:
    {
        "division": {
            "school": "coach_bio_text"
        }
    }
    """

    def __init__(self, cache: Dict[str, Dict[str, str]]) -> None:
        """
        Initialize coach service.

        Args:
            cache: Hierarchical coach data (division → school → coach bio)
        """
        self.cache = cache

    def get_divisions(self) -> List[str]:
        """
        Domain query: Get all available NCAA divisions.

        Returns:
            List of division names (e.g., ["D1", "D2", "D3"])
        """
        return list(self.cache.keys())

    def get_schools(self, division: str) -> List[str]:
        """
        Domain query: Get all schools in a specific division.

        Args:
            division: Division name (e.g., "D1")

        Returns:
            List of school names in that division
        """
        division_data = self.cache.get(division, {})
        return list(division_data.keys())