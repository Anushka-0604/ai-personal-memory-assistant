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


system_metric_service = SystemMetricService()