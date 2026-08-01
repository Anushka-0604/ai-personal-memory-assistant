from sqlalchemy.orm import Session

from app.services.retrieval_quality_service import (
    retrieval_quality_service,
)
from app.services.usage_dashboard_service import (
    usage_dashboard_service,
)
from app.services.system_metric_service import (
    system_metric_service,
)


class AIDashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        user_id: int,
    ):
        retrieval = (
            retrieval_quality_service.calculate_quality(
                db=db,
                user_id=user_id,
            )
        )

        usage = (
            usage_dashboard_service.get_dashboard(
                db=db,
                user_id=user_id,
            )
        )

        health = (
            system_metric_service.get_dashboard(
                db=db,
            )
        )

        return {
            "retrieval_quality": retrieval,
            "usage_dashboard": usage,
            "system_health": health,
        }


ai_dashboard_service = AIDashboardService()