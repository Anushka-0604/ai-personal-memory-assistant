from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.memory import Memory


class MemoryAnalyticsService:

    @staticmethod
    def get_statistics(
        db: Session,
        user_id: int,
    ):
        memories = (
            db.query(Memory)
            .filter(Memory.user_id == user_id)
            .all()
        )

        total = len(memories)

        archived = sum(
            1 for m in memories if m.is_archived
        )

        forgotten = sum(
            1 for m in memories if m.is_forgotten
        )

        avg_importance = (
            db.query(func.avg(Memory.importance))
            .filter(Memory.user_id == user_id)
            .scalar()
            or 0.0
        )

        avg_confidence = (
            db.query(func.avg(Memory.confidence))
            .filter(Memory.user_id == user_id)
            .scalar()
            or 0.0
        )

        total_access = (
            db.query(func.sum(Memory.access_count))
            .filter(Memory.user_id == user_id)
            .scalar()
            or 0
        )

        avg_access = (
            total_access / total
            if total
            else 0.0
        )

        category_distribution = {}

        for memory in memories:
            category = memory.category or "Unknown"
            category_distribution[category] = (
                category_distribution.get(category, 0) + 1
            )

        sentiment_distribution = {}

        for memory in memories:
            sentiment = memory.sentiment or "Unknown"
            sentiment_distribution[sentiment] = (
                sentiment_distribution.get(sentiment, 0) + 1
            )

        return {
            "total_memories": total,
            "archived_memories": archived,
            "forgotten_memories": forgotten,
            "average_importance": round(avg_importance, 2),
            "average_confidence": round(avg_confidence, 2),
            "category_distribution": category_distribution,
            "sentiment_distribution": sentiment_distribution,
            "total_access_count": total_access,
            "average_access_count": round(avg_access, 2),
        }


memory_analytics_service = MemoryAnalyticsService()