from pydantic import BaseModel, ConfigDict


class DocumentSearchResult(BaseModel):
    document_id: int
    document_name: str
    chunk_index: int
    content: str
    similarity: float

    model_config = ConfigDict(
        from_attributes=True,
    )


# Backward compatibility
DocumentCitation = DocumentSearchResult


class DocumentSearchResponse(BaseModel):
    results: list[DocumentSearchResult]