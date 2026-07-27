from datetime import datetime, timezone

from app.models.memory import Memory


class ArchiveService:
    """
    Archives memories that are old, rarely accessed,
    have low importance,
    and have low evidence.
    """

    def should_archive(self, memory: Memory) -> bool:
        # Never archive an already archived memory
        if memory.is_archived:
            return False

        # Calculate age in days
        age_days = (
            datetime.now(timezone.utc) - memory.updated_at
        ).days

        # Archiving rules
        return (
            age_days > 90
            and memory.importance < 0.40
            and memory.access_count < 3
            and memory.evidence_count <= 1
        )

    def archive(self, memory: Memory) -> None:
        memory.is_archived = True


archive_service = ArchiveService()