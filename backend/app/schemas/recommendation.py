from datetime import datetime

from pydantic import BaseModel


class RecommendedMemory(BaseModel):
    id: int
    content: str
    category: str | None = None
    importance: float | None = None
    updated_at: datetime

    class Config:
        from_attributes = True