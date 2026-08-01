from pydantic import BaseModel


class MemoryAnalyticsResponse(BaseModel):
    total_memories: int
    archived_memories: int
    forgotten_memories: int

    average_importance: float
    average_confidence: float

    category_distribution: dict[str, int]
    sentiment_distribution: dict[str, int]

    total_access_count: int
    average_access_count: float