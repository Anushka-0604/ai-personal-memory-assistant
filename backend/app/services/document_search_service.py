from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import (
    generate_embedding,
)


def semantic_document_search(
    db: Session,
    query: str,
    top_k: int = 5,
):
    query_embedding = generate_embedding(query)

    return (
        db.query(
            DocumentChunk,
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            ).label("distance"),
        )
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(top_k)
        .all()
    )