from pydantic import BaseModel


class MemoryInsights(BaseModel):
    total_memories: int
    total_categories: int
    archived_memories: int
    forgotten_memories: int

    most_used_category: str | None = None
    most_important_memory: str | None = None
    most_accessed_memory: str | None = None
    newest_memory: str | None = None