from datetime import datetime, timezone

from app.models.memory import Memory


class RankingService:
    """Ranks memories based on multiple signals."""

    def calculate_recency_score(self, memory: Memory) -> float:
        """Returns a score between 0 and 1 based on how recent the memory is."""

        now = datetime.now(timezone.utc)

        created_at = memory.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        age_days = (now - created_at).days

        if age_days <= 1:
            return 1.0
        elif age_days <= 7:
            return 0.9
        elif age_days <= 30:
            return 0.7
        elif age_days <= 90:
            return 0.5
        else:
            return 0.3

    def calculate_importance_score(self, memory: Memory) -> float:
        """Estimate the importance of a memory based on keywords."""

        content = memory.content.lower()

        important_keywords = [
            "interview",
            "meeting",
            "deadline",
            "exam",
            "project",
            "assignment",
            "goal",
            "appointment",
            "internship",
            "job",
            "doctor",
            "travel",
            "flight",
            "conference",
            "presentation",
        ]

        score = 0.3

        for keyword in important_keywords:
            if keyword in content:
                score += 0.1

        return min(score, 1.0)


ranking_service = RankingService()