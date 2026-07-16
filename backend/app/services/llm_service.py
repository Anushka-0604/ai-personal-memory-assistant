from google import genai
from google.genai.errors import APIError

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL
from app.core.logger import logger


class LLMService:
    """
    Service responsible for communicating with the Gemini LLM.
    """

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_response(self, prompt: str) -> str:
        """
        Sends the prompt to Gemini and returns the generated response.
        """
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            return response.text

        except APIError as e:
            logger.error(f"Gemini API Error: {e}")

            return (
                "I couldn't generate a final AI response because the "
                "LLM is currently unavailable. However, I found relevant "
                "memories that may help."
            )

        except Exception:
            logger.exception("Unexpected error while calling Gemini")

            return (
                "An unexpected error occurred while generating the response."
            )