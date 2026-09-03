from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: int = Field(
        ...,
        gt=0,
        description="Chat session ID",
    )

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's question",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of memories to retrieve",
    )


class RetrievedMemory(BaseModel):
    id: int
    content: str
    source: str
    similarity: float


class ChatResponse(BaseModel):
    answer: str
    retrieved_memories: list[RetrievedMemory]