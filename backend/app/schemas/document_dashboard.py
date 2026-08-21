from pydantic import BaseModel


class DocumentDashboard(BaseModel):
    total_documents: int
    total_chunks: int
    total_storage_bytes: int