import json

from app.schemas.extraction import MemoryExtraction
from app.services.llm_service import LLMService


class GeminiExtractor:
    """Uses Gemini to extract structured information from user memories."""

    def __init__(self):
        self.llm_service = LLMService()

    def extract(self, text: str) -> MemoryExtraction:
        prompt = f"""
You are an AI memory extraction assistant.

Extract important information from the following memory.

Return ONLY valid JSON.

Schema:
{{
    "people": [],
    "organizations": [],
    "locations": [],
    "dates": [],
    "events": [],
    "tasks": [],
    "goals": [],
    "preferences": [],
    "summary": ""
}}

Memory:
{text}
"""

        response = self.llm_service.generate_response(prompt)

        try:
            # Remove markdown code blocks if Gemini returns them
            cleaned_response = response.strip()

            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.replace("```json", "", 1)

            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.replace("```", "", 1)

            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]

            cleaned_response = cleaned_response.strip()

            data = json.loads(cleaned_response)

            return MemoryExtraction(**data)

        except Exception:
            # Return an empty extraction if the response
            # is invalid or the API is unavailable.
            return MemoryExtraction()