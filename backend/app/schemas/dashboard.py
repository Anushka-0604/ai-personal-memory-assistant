from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_memories: int
    active_memories: int
    archived_memories: int

    top_category: str | None = None
    least_used_category: str | None = None

    archive_percentage: float

    insight: str