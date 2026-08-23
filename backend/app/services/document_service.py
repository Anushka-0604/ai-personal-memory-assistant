import time

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.classification_service import (
    classification_service,
)
from app.services.document_chunking_service import (
    document_chunking_service,
)
from app.services.document_extraction_service import (
    document_extraction_service,
)
from app.services.embedding_service import (
    generate_embedding,
)
from app.services.keyword_extraction_service import (
    keyword_extraction_service,
)
from app.services.ner_service import (
    ner_service,
)
from app.services.relationship_extraction_service import (
    relationship_extraction_service,
)
from app.services.system_metric_service import (
    system_metric_service,
)


# =====================================================
# Create Document
# =====================================================

def create_document(
    db: Session,
    user_id: int,
    filename: str,
    original_filename: str,
    file_type: str,
    file_size: int,
    file_path: str,
):
    processing_start = time.perf_counter()

    extracted_text = (
        document_extraction_service.extract_text(
            file_path
        )
    )

    # =================================================
    # Document Classification
    # =================================================

    document_category = (
        classification_service.classify_document(
            text=extracted_text,
            filename=original_filename,
        )
    )

    # =================================================
    # Keyword Extraction
    # =================================================

    keywords = (
        keyword_extraction_service.extract_keywords(
            text=extracted_text,
            top_k=10,
        )
    )

    # =================================================
    # Named Entity Recognition
    # =================================================

    entities = (
        ner_service.extract_entities(
            extracted_text
        )
    )

    # =================================================
    # Relationship Extraction
    # =================================================

    relationships = (
        relationship_extraction_service.extract_relationships(
            extracted_text,
            entities,
        )
    )

    # =================================================
    # Create Document with Enriched Metadata
    # =================================================

    document = Document(
        user_id=user_id,
        filename=filename,
        original_filename=original_filename,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path,
        extracted_text=extracted_text,
        document_category=document_category,
        keywords=keywords,
        entities=entities,
        relationships=relationships,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # =================================================
    # Document Chunking
    # =================================================

    chunks = (
        document_chunking_service.chunk_text(
            extracted_text
        )
    )

    # =================================================
    # Generate Embeddings
    # =================================================

    embedding_start = time.perf_counter()

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(
            chunk
        )

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk,
            embedding=embedding,
        )

        db.add(document_chunk)

    embedding_time = (
        time.perf_counter() - embedding_start
    ) * 1000

    db.commit()

    # =================================================
    # Performance Metrics
    # =================================================

    processing_time = (
        time.perf_counter() - processing_start
    ) * 1000

    system_metric_service.log(
        db=db,
        metric_name="document_processing_time",
        metric_value=processing_time,
        unit="ms",
    )

    system_metric_service.log(
        db=db,
        metric_name="document_embedding_time",
        metric_value=embedding_time,
        unit="ms",
    )

    return document


# =====================================================
# Get All Documents
# =====================================================

def get_documents(
    db: Session,
    user_id: int,
):
    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .all()
    )


# =====================================================
# Get Document By ID
# =====================================================

def get_document_by_id(
    db: Session,
    document_id: int,
    user_id: int,
):
    return (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user_id,
        )
        .first()
    )


# =====================================================
# Delete Document
# =====================================================

def delete_document(
    db: Session,
    document: Document,
):
    db.delete(document)
    db.commit()