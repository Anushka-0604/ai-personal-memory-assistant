from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class MemoryCreate(BaseModel):
    content: str
    source: str = "chat"


class MemoryUpdate(BaseModel):
    content: str
    source: str


class MemoryResponse(BaseModel):
    id: int
    user_id: int
    content: str
    source: str

    # Existing metadata
    temporal_date: date | None = None
    extracted_data: dict | None = None

    # Module 2 & Module 4 metadata
    category: str | None = None
    importance: float | None = None
    tags: list | None = None
    sentiment: str | None = None
    confidence: float | None = None
    access_count: int
    last_accessed: datetime | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Semantic Search Schemas
# ==========================

class MemorySearchRequest(BaseModel):
    query: str
    top_k: int = 5


class MemorySearchResult(BaseModel):
    id: int
    content: str
    source: str
    category: str | None = None
    temporal_date: date | None = None
    similarity: float
    recency_score: float
    importance_score: float
    final_score: float

    model_config = ConfigDict(from_attributes=True)