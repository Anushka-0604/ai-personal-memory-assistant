from datetime import datetime, timezone

from app.models.memory import Memory


class ForgettingService:
    """
    Marks archived memories as forgotten
    after a long retention period.
    """

    def should_forget(
        self,
        memory: Memory,
    ) -> bool:

        # Already forgotten
        if memory.is_forgotten:
            return False

        # Must already be archived
        if not memory.is_archived:
            return False

        age_days = (
            datetime.now(timezone.utc)
            - memory.updated_at
        ).days

        return (
            age_days > 365
            and memory.access_count == 0
            and memory.evidence_count <= 1
        )

    def forget(
        self,
        memory: Memory,
    ) -> None:
        memory.is_forgotten = True


forgetting_service = ForgettingService() 