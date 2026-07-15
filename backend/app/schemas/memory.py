from datetime import datetime

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
    similarity: float

    model_config = ConfigDict(from_attributes=True)