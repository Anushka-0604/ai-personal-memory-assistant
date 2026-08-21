from pydantic import BaseModel


class DocumentUsageStatistics(BaseModel):
    total_documents: int
    total_chunks: int
    total_storage_bytes: int