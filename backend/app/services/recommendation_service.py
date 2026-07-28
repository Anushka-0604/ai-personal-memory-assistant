from sqlalchemy.orm import Session

from app.models.memory import Memory


class RecommendationService:
    def _get_reason(
        self,
        memory: Memory,
    ) -> str:
        if memory.importance is not None and memory.importance >= 8:
            return "High importance"

        if memory.access_count >= 5:
            return "Frequently accessed"

        return "Recently updated"

    def get_recommended_memories(
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
            )
            .order_by(
                Memory.importance.desc(),
                Memory.updated_at.desc(),
            )
            .limit(limit)
            .all()
        )

        recommendations = []

        for memory in memories:
            recommendations.append(
                {
                    "id": memory.id,
                    "content": memory.content,
                    "category": memory.category,
                    "importance": memory.importance,
                    "reason": self._get_reason(memory),
                    "updated_at": memory.updated_at,
                }
            )

        return recommendations


recommendation_service = RecommendationService()