from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.document_extraction_service import (
    document_extraction_service,
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