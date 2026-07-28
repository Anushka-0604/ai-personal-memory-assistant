from datetime import datetime

from pydantic import BaseModel


class ReviewMemory(BaseModel):
    id: int
    content: str
    category: str | None = None
    last_accessed: datetime | None = None
    access_count: int
    reason: str

    class Config:
        from_attributes = True