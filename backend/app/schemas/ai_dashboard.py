from pydantic import BaseModel


class AIDashboardResponse(BaseModel):
    retrieval_quality: dict
    usage_dashboard: dict
    system_health: dict