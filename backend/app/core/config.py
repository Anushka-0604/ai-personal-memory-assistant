from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

PROJECT_NAME = "AI Personal Memory & Decision Assistant API"

DATABASE_URL = os.getenv("DATABASE_URL")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

SECRET_KEY = "change_this_to_a_long_random_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

RAG_SIMILARITY_THRESHOLD = float(
    os.getenv("RAG_SIMILARITY_THRESHOLD", 0.70)
)

MAX_CHAT_HISTORY = int(
    os.getenv("MAX_CHAT_HISTORY", 10)
)

NEO4J_URI = os.getenv("NEO4J_URI")

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

CONVERSATION_HISTORY_LIMIT = int(
    os.getenv("CONVERSATION_HISTORY_LIMIT", 10)
)


CONVERSATION_SUMMARIZATION_THRESHOLD = int(
    os.getenv(
        "CONVERSATION_SUMMARIZATION_THRESHOLD",
        20,
    )
)