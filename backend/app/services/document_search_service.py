from datetime import date

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.document_search import (
    DocumentCitation,
)
from app.services.embedding_service import (
    generate_embedding,
)


def semantic_document_search(
    db: Session,
    query: str,
    top_k: int = 5,
    document_id: int | None = None,
    file_type: str | None = None,
    upload_date: date | None = None,
) -> list[DocumentCitation]:

    query_embedding = generate_embedding(query)

    search_query = (
        db.query(
            Document,
            DocumentChunk,
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            ).label("distance"),
        )
        .join(
            DocumentChunk,
            Document.id == DocumentChunk.document_id,
        )
    )

    if document_id is not None:
        search_query = search_query.filter(
            Document.id == document_id
        )

    if file_type is not None:
        search_query = search_query.filter(
            Document.file_type == file_type
        )

    if upload_date is not None:
        search_query = search_query.filter(
            Document.created_at >= upload_date,
        )

    results = (
        search_query
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(top_k)
        .all()
    )

    citations = []

    for (
        document,
        chunk,
        distance,
    ) in results:

        citations.append(
            DocumentCitation(
                document_id=document.id,
                document_name=document.original_filename,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                similarity=round(
                    1 - float(distance),
                    4,
                ),
            )
        )

    return citations