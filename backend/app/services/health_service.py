import os
import shutil

import psutil
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.services.llm_service import LLMService
from app.services.embedding_service import model

class HealthService:

    @staticmethod
    def get_health(db: Session):

        # Database
        try:
            db.execute(text("SELECT 1"))
            database = "Healthy"
        except Exception:
            database = "Unhealthy"

        # CPU
        cpu = psutil.cpu_percent(interval=1)

        # Memory
        memory = psutil.virtual_memory().percent

        # Disk
        disk = shutil.disk_usage(os.getcwd())

        disk_percent = round(
            (disk.used / disk.total) * 100,
            2,
        )

        # Embedding Model
        try:
            _ = model
            embedding_model = "Healthy"
        except Exception:
            embedding_model = "Unhealthy"

        # LLM Service
        try:
            _ = LLMService()
            llm_service = "Healthy"
        except Exception:
            llm_service = "Unhealthy"

        return {
            "database": database,
            "embedding_model": embedding_model,
            "llm_service": llm_service,
            "cpu_percent": cpu,
            "memory_percent": memory,
            "disk_percent": disk_percent,
}


health_service = HealthService()