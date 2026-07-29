from datetime import datetime

from pydantic import BaseModel


class TimelineMemory(BaseModel):
    id: int
    content: str
    category: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True