from pydantic import BaseModel


class DocumentChatRequest(BaseModel):
    question: str
    top_k: int = 5


class DocumentChatResponse(BaseModel):
    answer: str
    context: str