from datetime import datetime

from pydantic import BaseModel


class AIRequestLogResponse(BaseModel):
    id: int
    query: str

    retrieval_count: int
    selected_count: int

    average_similarity: float
    average_importance: float
    average_context_score: float

    precision_score: float
    recall_score: float

    response_generated: bool
    response_length: int

    embedding_time_ms: float
    retrieval_time_ms: float
    ranking_time_ms: float
    context_time_ms: float
    prompt_time_ms: float
    llm_time_ms: float
    total_time_ms: float

    created_at: datetime

    model_config = {
        "from_attributes": True
    }