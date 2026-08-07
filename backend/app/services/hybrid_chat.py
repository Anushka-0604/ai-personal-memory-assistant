from pydantic import BaseModel


class HybridChatRequest(BaseModel):
    question: str
    top_k: int = 5


class HybridChatResponse(BaseModel):
    answer: str
    context: str
    memory_count: int
    document_count: int