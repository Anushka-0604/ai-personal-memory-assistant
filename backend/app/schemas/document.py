from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    file_path: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)