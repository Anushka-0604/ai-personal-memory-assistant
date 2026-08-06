from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.document_chunking_service import (
    document_chunking_service,
)
from app.services.document_extraction_service import (
    document_extraction_service,
)
from app.services.embedding_service import (
    generate_embedding,
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
    extracted_text = (
        document_extraction_service.extract_text(
            file_path
        )
    )

    document = Document(
        user_id=user_id,
        filename=filename,
        original_filename=original_filename,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path,
        extracted_text=extracted_text,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    chunks = (
        document_chunking_service.chunk_text(
            extracted_text
        )
    )

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(
            chunk
        )

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            page_number=None,
            content=chunk,
            embedding=embedding,
        )

        db.add(document_chunk)

    db.commit()

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