import time

from app.core.logger import logger


class ObservabilityService:

    @staticmethod
    def start_trace():
        return time.perf_counter()

    @staticmethod
    def end_trace(start_time: float) -> float:
        return (time.perf_counter() - start_time) * 1000

    @staticmethod
    def log_stage(
        stage: str,
        duration_ms: float,
    ):
        logger.info(
            f"[TRACE] {stage}: {duration_ms:.2f} ms"
        )


observability_service = ObservabilityService()