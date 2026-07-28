from pydantic import BaseModel


class MemoryStatistics(BaseModel):
    total_memories: int
    active_memories: int
    archived_memories: int


class CategoryDistribution(BaseModel):
    category: str | None = None
    count: int