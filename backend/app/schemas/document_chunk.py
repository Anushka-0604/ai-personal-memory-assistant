from pydantic import BaseModel


class DocumentChunkMetadata(BaseModel):
    document_id: int
    chunk_index: int
    paragraph_index: int
    sentence_count: int
    character_count: int
    content: str