from datetime import datetime, timezone


class PersonalizationService:
    """
    Computes a personalization score for
    each memory using user interaction
    and memory metadata.
    """

    def calculate_score(
        self,
        memory,
    ) -> float:

        importance = (
            memory.importance
            if memory.importance is not None
            else 0.5
        )

        confidence = (
            memory.confidence
            if memory.confidence is not None
            else 0.5
        )

        access = min(
            memory.access_count / 20,
            1.0,
        )

        if memory.last_accessed:

            days = (
                datetime.now(timezone.utc)
                - memory.last_accessed
            ).days

            recency = max(
                0.0,
                1 - (days / 30),
            )

        else:

            recency = 0.0

        score = (
            0.40 * importance
            + 0.25 * access
            + 0.20 * recency
            + 0.15 * confidence
        )

        return round(score, 4)


personalization_service = (
    PersonalizationService()
)