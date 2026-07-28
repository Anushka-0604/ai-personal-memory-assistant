from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.memory import Memory


class ReviewService:
    def _get_reason(
        self,
        memory: Memory,
    ) -> str:
        if memory.last_accessed is None:
            return "Never reviewed"

        days_since_access = (
            datetime.now(memory.last_accessed.tzinfo)
            - memory.last_accessed
        ).days

        if days_since_access >= 30:
            return "Not reviewed for over 30 days"

        if memory.access_count <= 1:
            return "Needs reinforcement"

        return "Review recommended"

    def get_review_queue(
        self,
        db: Session,
        user_id: int,
        limit: int = 5,
    ):
        memories = (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.is_archived == False,
                Memory.is_forgotten == False,
            )
            .order_by(
                Memory.last_accessed.asc().nullsfirst(),
                Memory.access_count.asc(),
                Memory.updated_at.asc(),
            )
            .limit(limit)
            .all()
        )

        review_queue = []

        for memory in memories:
            review_queue.append(
                {
                    "id": memory.id,
                    "content": memory.content,
                    "category": memory.category,
                    "last_accessed": memory.last_accessed,
                    "access_count": memory.access_count,
                    "reason": self._get_reason(memory),
                }
            )

        return review_queue


review_service = ReviewService()