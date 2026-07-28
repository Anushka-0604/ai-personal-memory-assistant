from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.memory import Memory


class AnalyticsService:
    """Provides analytics about a user's memories."""

    def get_memory_statistics(
        self,
        db: Session,
        user_id: int,
    ):
        total_memories = (
            db.query(Memory)
            .filter(Memory.user_id == user_id)
            .count()
        )

        archived_memories = (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.is_archived == True,
            )
            .count()
        )

        active_memories = (
            total_memories - archived_memories
        )

        return {
            "total_memories": total_memories,
            "active_memories": active_memories,
            "archived_memories": archived_memories,
        }

    def get_category_distribution(
        self,
        db: Session,
        user_id: int,
    ):
        results = (
            db.query(
                Memory.category,
                func.count(Memory.id),
            )
            .filter(
                Memory.user_id == user_id
            )
            .group_by(
                Memory.category
            )
            .all()
        )

        return [
            {
                "category": category,
                "count": count,
            }
            for category, count in results
        ]


analytics_service = AnalyticsService()