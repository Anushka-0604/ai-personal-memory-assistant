from datetime import date

from sqlalchemy.orm import Session

from app.models.memory import Memory


class TimelineService:
    def get_timeline(
        self,
        db: Session,
        user_id: int,
        limit: int = 20,
        page: int = 1,
        category: str | None = None,
        search: str | None = None,
        include_archived: bool = False,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        query = (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
            )
        )

        if not include_archived:
            query = query.filter(
                Memory.is_archived == False,
            )

        if category:
            query = query.filter(
                Memory.category.ilike(category),
            )

        if search:
            query = query.filter(
                Memory.content.ilike(f"%{search}%")
            )

        if start_date:
            query = query.filter(
                Memory.created_at >= start_date,
            )

        if end_date:
            query = query.filter(
                Memory.created_at <= end_date,
            )

        offset = (page - 1) * limit

        memories = (
            query.order_by(
                Memory.created_at.desc(),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        return memories


timeline_service = TimelineService()