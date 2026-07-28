from datetime import datetime

from pydantic import BaseModel


class UserInteractionBase(BaseModel):
    memory_id: int
    interaction_type: str


class UserInteractionCreate(UserInteractionBase):
    pass


class UserInteractionResponse(UserInteractionBase):
    id: int
    user_id: int
    weight: int
    created_at: datetime

    class Config:
        from_attributes = True