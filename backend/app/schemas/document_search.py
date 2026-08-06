from pydantic import BaseModel, ConfigDict


class DocumentCitation(BaseModel):
    document_id: int
    document_name: str
    chunk_index: int
    content: str
    similarity: float

    model_config = ConfigDict(
        from_attributes=True,
    )


class DocumentSearchResponse(BaseModel):
    results: list[DocumentCitation]