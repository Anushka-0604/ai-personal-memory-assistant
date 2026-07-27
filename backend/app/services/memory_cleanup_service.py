from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.services.archive_service import archive_service
from app.services.forgetting_service import (
    forgetting_service,
)


class MemoryCleanupService:
    """
    Performs long-term memory maintenance.

    Responsibilities:
    - Archive inactive memories.
    - Forget archived memories after
      the retention period.
    """

    def cleanup(
        self,
        db: Session,
    ) -> dict:
        archived = 0
        forgotten = 0

        memories = db.query(Memory).all()

        for memory in memories:

            # Archive eligible memories
            if archive_service.should_archive(memory):
                archive_service.archive(memory)
                archived += 1

            # Forget eligible archived memories
            if forgetting_service.should_forget(memory):
                forgetting_service.forget(memory)
                forgotten += 1

        db.commit()

        return {
            "archived": archived,
            "forgotten": forgotten,
            "processed": len(memories),
        }


memory_cleanup_service = MemoryCleanupService()
