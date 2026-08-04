from pydantic import BaseModel, ConfigDict


class DocumentSearchResult(BaseModel):
    document_id: int
    chunk_index: int
    content: str
    similarity: float

    model_config = ConfigDict(
        from_attributes=True,
    )