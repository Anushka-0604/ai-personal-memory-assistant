from datetime import date

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.document_search import (
    DocumentSearchResult,
)
from app.services.document_ranking_service import (
    document_ranking_service,
)
from app.services.embedding_service import (
    generate_embedding,
)
from app.services.multi_document_retrieval_service import (
    multi_document_retrieval_service,
)


def semantic_document_search(
    db: Session,
    query: str,
    top_k: int = 5,
    document_id: int | None = None,
    file_type: str | None = None,
    upload_date: date | None = None,
    group_by_document: bool = False,
):
    """
    Perform semantic search over document chunks.

    The query is converted into an embedding and compared
    against stored document chunk embeddings using cosine
    distance.

    Duplicate chunks are removed before ranking so that
    repeated document content does not occupy multiple
    retrieval slots.
    """

    query_embedding = generate_embedding(query)

    search_query = (
        db.query(
            DocumentChunk,
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            ).label("distance"),
        )
        .join(
            Document,
            Document.id == DocumentChunk.document_id,
        )
        .filter(
            DocumentChunk.embedding.is_not(None)
        )
    )

    # =====================================================
    # Optional Filters
    # =====================================================

    if document_id is not None:
        search_query = search_query.filter(
            DocumentChunk.document_id == document_id
        )

    if file_type is not None:
        search_query = search_query.filter(
            Document.file_type == file_type
        )

    if upload_date is not None:
        search_query = search_query.filter(
            Document.created_at >= upload_date
        )

    # =====================================================
    # Vector Search
    # =====================================================

    rows = (
        search_query
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(top_k * 3)
        .all()
    )

    results = []

    # =====================================================
    # Remove Duplicate Chunks
    # =====================================================

    seen_chunks = set()

    for chunk, distance in rows:

        # Use document ID + chunk content as the
        # duplicate detection key.
        duplicate_key = (
            chunk.document_id,
            chunk.content.strip(),
        )

        if duplicate_key in seen_chunks:
            continue

        seen_chunks.add(duplicate_key)

        similarity = max(
            0.0,
            1.0 - float(distance),
        )

        results.append(
            DocumentSearchResult(
                document_id=chunk.document_id,
                document_name=chunk.document.original_filename,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                similarity=similarity,
            )
        )

        # Keep the requested number of unique results.
        if len(results) >= top_k:
            break

    # =====================================================
    # Rank Results
    # =====================================================

    ranked_results = (
        document_ranking_service.rank(
            results
        )
    )

    # =====================================================
    # Optional Grouping
    # =====================================================

    if group_by_document:
        return (
            multi_document_retrieval_service.group_by_document(
                ranked_results
            )
        )

    return ranked_results