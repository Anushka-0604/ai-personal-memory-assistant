from google import genai
from google.genai.errors import APIError

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL
from app.core.logger import logger


class LLMService:
    """
    Service responsible for communicating with the Gemini LLM.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_response(
        self,
        prompt: str,
    ) -> str:
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
            logger.error(
                "Gemini API Error: %s",
                e,
            )

            # Re-raise the error during development so that
            # the actual Gemini failure is visible in the
            # backend terminal.
            raise

        except Exception as e:
            logger.exception(
                "Unexpected error while calling Gemini: %s",
                e,
            )

            raise