from sqlalchemy.orm import Session

from app.models.memory import Memory


class TimelineService:
    def get_timeline(
        self,
        db: Session,
        user_id: int,
        limit: int = 20,
    ):
        memories = (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
            )
            .order_by(
                Memory.created_at.desc(),
            )
            .limit(limit)
            .all()
        )

        return memories


timeline_service = TimelineService()