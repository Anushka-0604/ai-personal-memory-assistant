from google import genai

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL


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

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return response.text