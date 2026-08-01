from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ai_request_log import AIRequestLog


class EvaluationService:

    @staticmethod
    def log_request(
        db: Session,
        **kwargs,
    ) -> AIRequestLog:

        log = AIRequestLog(**kwargs)

        db.add(log)
        db.commit()
        db.refresh(log)

        return log

    @staticmethod
    def get_latest(
        db: Session,
        user_id: int,
        limit: int = 20,
    ):
        return (
            db.query(AIRequestLog)
            .filter(AIRequestLog.user_id == user_id)
            .order_by(AIRequestLog.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_summary(
        db: Session,
        user_id: int,
    ):
        total_requests = (
            db.query(func.count(AIRequestLog.id))
            .filter(AIRequestLog.user_id == user_id)
            .scalar()
            or 0
        )

        avg_response_time = (
            db.query(func.avg(AIRequestLog.total_time_ms))
            .filter(AIRequestLog.user_id == user_id)
            .scalar()
            or 0.0
        )

        avg_similarity = (
            db.query(func.avg(AIRequestLog.average_similarity))
            .filter(AIRequestLog.user_id == user_id)
            .scalar()
            or 0.0
        )

        success_count = (
            db.query(func.count(AIRequestLog.id))
            .filter(
                AIRequestLog.user_id == user_id,
                AIRequestLog.response_generated.is_(True),
            )
            .scalar()
            or 0
        )

        success_rate = (
            (success_count / total_requests) * 100
            if total_requests
            else 0.0
        )

        return {
            "total_requests": total_requests,
            "average_response_time_ms": round(avg_response_time, 2),
            "average_similarity": round(avg_similarity, 4),
            "success_rate": round(success_rate, 2),
        }