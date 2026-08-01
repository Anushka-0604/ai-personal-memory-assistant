from pydantic import BaseModel


class UsageDashboard(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time_ms: float
    average_similarity: float
    average_response_length: float