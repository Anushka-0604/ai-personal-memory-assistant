from datetime import date

from sqlalchemy.orm import Session

from app.models.memory import Memory


class TemporalQueryService:
    """Provides temporal queries over stored memories."""

    def get_memories_for_date(
        self,
        db: Session,
        user_id: int,
        target_date: date,
    ):
        return (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.temporal_date == target_date,
            )
            .all()
        )


temporal_query_service = TemporalQueryService()