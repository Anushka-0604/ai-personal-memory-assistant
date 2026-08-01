from pydantic import BaseModel


class RetrievalQualityResponse(BaseModel):
    average_similarity: float
    average_selected: float
    average_retrieved: float
    average_response_length: float
    response_rate: float