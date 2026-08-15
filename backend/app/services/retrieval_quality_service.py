from sqlalchemy.orm import Session

from app.models.ai_request_log import AIRequestLog


class RetrievalQualityService:

    @staticmethod
    def calculate_quality(
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
                "average_similarity": 0.0,
                "average_selected": 0.0,
                "average_retrieved": 0.0,
                "average_response_length": 0.0,
                "response_rate": 0.0,
            }

        total = len(logs)

        return {
            "average_similarity": round(
                sum(
                    log.average_similarity
                    for log in logs
                ) / total,
                4,
            ),
            "average_selected": round(
                sum(
                    log.selected_count
                    for log in logs
                ) / total,
                2,
            ),
            "average_retrieved": round(
                sum(
                    log.retrieval_count
                    for log in logs
                ) / total,
                2,
            ),
            "average_response_length": round(
                sum(
                    log.response_length
                    for log in logs
                ) / total,
                2,
            ),
            "response_rate": round(
                (
                    sum(
                        1
                        for log in logs
                        if log.response_generated
                    )
                    / total
                )
                * 100,
                2,
            ),
        }


retrieval_quality_service = RetrievalQualityServiceeee()