from sqlalchemy.orm import Session

from app.models.ai_request_log import AIRequestLog


class UsageDashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        user_id: int,
    ):
        logs = (
            db.query(AIRequestLog)
            .filter(
                AIRequestLog.user_id == user_id
            )
            .all()
        )

        if not logs:
            return {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time_ms": 0.0,
                "average_similarity": 0.0,
                "average_response_length": 0.0,
            }

        total = len(logs)

        successful = sum(
            1
            for log in logs
            if log.response_generated
        )

        failed = total - successful

        return {
            "total_requests": total,
            "successful_requests": successful,
            "failed_requests": failed,
            "average_response_time_ms": round(
                sum(
                    log.total_time_ms
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
            "average_response_length": round(
                sum(
                    log.response_length
                    for log in logs
                ) / total,
                2,
            ),
        }


usage_dashboard_service = UsageDashboardService()