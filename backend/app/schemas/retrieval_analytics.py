from pydantic import BaseModel


class RetrievalAnalyticsResponse(BaseModel):
    total_retrievals: int
    average_retrieved: float
    average_selected: float
    average_similarity: float
    average_retrieval_time_ms: float