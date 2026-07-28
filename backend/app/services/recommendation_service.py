from sqlalchemy.orm import Session

from app.models.memory import Memory


class RecommendationService:
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

        return memories


recommendation_service = RecommendationService()