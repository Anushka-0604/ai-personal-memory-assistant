from sqlalchemy.orm import Session

from app.models.retrieval_log import RetrievalLog


class RetrievalAnalyticsService:

    @staticmethod
    def log(
        db: Session,
        **kwargs,
    ) -> RetrievalLog:

        log = RetrievalLog(**kwargs)

        db.add(log)
        db.commit()
        db.refresh(log)

        return log


retrieval_analytics_service = RetrievalAnalyticsService()
