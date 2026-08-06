import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from app.core.logger import logger
from app.services.cache_service import cache_service

load_dotenv()

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2",
)

logger.info(f"Loading embedding model: {MODEL_NAME}")

model = SentenceTransformer(
    MODEL_NAME,
    local_files_only=True,
)

logger.info("Embedding model loaded successfully!")


def generate_embedding(text: str) -> list[float]:
    """
    Generate a vector embedding for the given text.
    """

    cached_embedding = cache_service.get_embedding(text)

    if cached_embedding is not None:
        return cached_embedding

    embedding = model.encode(
        text,
        convert_to_numpy=True,
    ).tolist()

    cache_service.set_embedding(
        text,
        embedding,
    )

    return embedding