from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.services.embedding_service import generate_embedding


class DuplicateDetectionService:
    """
    Detects duplicate memories using semantic similarity.

    A memory is considered a duplicate if its embedding is
    sufficiently similar to an existing memory belonging to
    the same user.
    """

    # Similarity threshold (can later move to config.py)
    DUPLICATE_THRESHOLD = 0.92

    def find_duplicate(
        self,
        db: Session,
        user_id: int,
        content: str,
    ):
        """
        Returns:
            {
                "is_duplicate": bool,
                "memory": Memory | None,
                "similarity": float
            }
        """

        embedding = generate_embedding(content)

        result = (
            db.query(
                Memory,
                Memory.embedding.cosine_distance(
                    embedding
                ).label("distance"),
            )
            .filter(Memory.user_id == user_id)
            .order_by(
                Memory.embedding.cosine_distance(
                    embedding
                )
            )
            .first()
        )

        if result is None:
            return {
                "is_duplicate": False,
                "memory": None,
                "similarity": 0.0,
            }

        memory, distance = result

        similarity = 1 - distance

        if similarity >= self.DUPLICATE_THRESHOLD:
            return {
                "is_duplicate": True,
                "memory": memory,
                "similarity": similarity,
            }

        return {
            "is_duplicate": False,
            "memory": None,
            "similarity": similarity,
        }


duplicate_detection_service = DuplicateDetectionService()