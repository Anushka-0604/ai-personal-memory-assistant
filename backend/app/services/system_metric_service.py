from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.system_metric import SystemMetric


class SystemMetricService:

    @staticmethod
    def log(
        db: Session,
        metric_name: str,
        metric_value: float,
        unit: str,
    ):
        metric = SystemMetric(
            metric_name=metric_name,
            metric_value=metric_value,
            unit=unit,
        )

        db.add(metric)
        db.commit()
        db.refresh(metric)

        return metric

    @staticmethod
    def get_dashboard(
        db: Session,
    ):
        metrics = db.query(SystemMetric).all()

        if not metrics:
            return {
                "total_metrics": 0,
                "average_metric_value": 0.0,
                "latest_metric": None,
            }

        latest = (
            db.query(SystemMetric)
            .order_by(SystemMetric.created_at.desc())
            .first()
        )

        average = (
            db.query(
                func.avg(SystemMetric.metric_value)
            ).scalar()
            or 0.0
        )

        return {
            "total_metrics": len(metrics),
            "average_metric_value": round(
                float(average),
                2,
            ),
            "latest_metric": (
                latest.metric_name
                if latest
                else None
            ),
        }


system_metric_service = SystemMetricService()