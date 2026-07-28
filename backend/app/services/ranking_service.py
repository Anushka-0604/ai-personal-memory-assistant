from datetime import datetime, timezone

from app.models.memory import Memory


class RankingService:
    """Ranks memories based on multiple signals."""

    IMPORTANT_KEYWORDS = [
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

    def calculate_recency_score(self, memory: Memory) -> float:
        """Returns a score between 0 and 1 based on how recent the memory is."""

        now = datetime.now(timezone.utc)

        created_at = memory.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(
                tzinfo=timezone.utc
            )

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

    def calculate_importance(
        self,
        text: str,
    ) -> float:
        """Calculate importance directly from text."""

        text = text.lower()

        score = 0.3

        for keyword in self.IMPORTANT_KEYWORDS:
            if keyword in text:
                score += 0.1

        return min(score, 1.0)

    def calculate_memory_decay(
        self,
        memory: Memory,
    ) -> float:
        """
        Returns a decay multiplier between 0 and 1.

        Recently accessed memories decay less.
        Older memories decay more.
        """

        now = datetime.now(timezone.utc)

        last_access = (
            memory.last_accessed
            or memory.created_at
        )

        if last_access.tzinfo is None:
            last_access = last_access.replace(
                tzinfo=timezone.utc
            )

        days = (now - last_access).days

        if days <= 7:
            return 1.0
        elif days <= 30:
            return 0.95
        elif days <= 90:
            return 0.85
        elif days <= 180:
            return 0.70
        else:
            return 0.50

    def calculate_importance_score(
        self,
        memory: Memory,
    ) -> float:
        """
        Final importance score after applying memory decay.
        """

        base_score = (
            memory.importance
            if memory.importance is not None
            else self.calculate_importance(
                memory.content
            )
        )

        decay = self.calculate_memory_decay(
            memory
        )

        return base_score * decay

    def calculate_interaction_score(
        self,
        memory: Memory,
    ) -> float:
        """
        Score based on how frequently the user interacts
        with a memory.
        """

        access_count = memory.access_count or 0

        if access_count >= 100:
            return 1.0
        elif access_count >= 50:
            return 0.9
        elif access_count >= 20:
            return 0.8
        elif access_count >= 10:
            return 0.7
        elif access_count >= 5:
            return 0.6
        elif access_count >= 1:
            return 0.5

        return 0.3

    def calculate_final_score(
        self,
        similarity_score: float,
        memory: Memory,
    ) -> float:
        """
        Final ranking score combining semantic similarity,
        importance, recency and interaction history.
        """

        importance_score = self.calculate_importance_score(
            memory
        )

        recency_score = self.calculate_recency_score(
            memory
        )

        interaction_score = self.calculate_interaction_score(
            memory
        )

        final_score = (
            (similarity_score * 0.50)
            + (importance_score * 0.20)
            + (recency_score * 0.15)
            + (interaction_score * 0.15)
        )

        return round(final_score, 4)


ranking_service = RankingService()