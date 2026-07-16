from openai import OpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model=OPENAI_MODEL,
    input="Say hello in one sentence."
)

print(response.output_text)