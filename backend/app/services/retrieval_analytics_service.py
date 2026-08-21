from sqlalchemy import func
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

    @staticmethod
    def get_statistics(
        db: Session,
        user_id: int,
    ):
        logs = (
            db.query(RetrievalLog)
            .filter(
                RetrievalLog.user_id == user_id
            )
            .all()
        )

        if not logs:
            return {
                "total_retrievals": 0,
                "average_retrieved": 0.0,
                "average_selected": 0.0,
                "average_similarity": 0.0,
                "average_retrieval_time_ms": 0.0,
            }

        total = len(logs)

        return {
            "total_retrievals": total,
            "average_retrieved": round(
                sum(
                    log.retrieved_count
                    for log in logs
                ) / total,
                2,
            ),
            "average_selected": round(
                sum(
                    log.selected_count
                    for log in logs
                ) / total,
                2,
            ),
            "average_similarity": round(
                sum(
                    log.average_similarity
                    for log in logs
                ) / total,
                4,
            ),
            "average_retrieval_time_ms": round(
                sum(
                    log.retrieval_time_ms
                    for log in logs
                ) / total,
                2,
            ),
        }


retrieval_analytics_service = RetrievalAnalyticsService()