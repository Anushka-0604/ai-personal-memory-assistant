import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2",
)

print(f"Loading embedding model: {MODEL_NAME}")

model = SentenceTransformer(
    MODEL_NAME,
    local_files_only=True,
)

print("Embedding model loaded successfully!")


def generate_embedding(text: str) -> list[float]:
    """
    Generate a vector embedding for the given text.
    """
    embedding = model.encode(
        text,
        convert_to_numpy=True,
    )
    return embedding.tolist()