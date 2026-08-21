from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class DocumentDashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        user_id: int,
    ):
        total_documents = (
            db.query(Document)
            .filter(
                Document.user_id == user_id
            )
            .count()
        )

        total_chunks = (
            db.query(DocumentChunk)
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .filter(
                Document.user_id == user_id
            )
            .count()
        )

        total_storage = (
            db.query(
                func.coalesce(
                    func.sum(Document.file_size),
                    0,
                )
            )
            .filter(
                Document.user_id == user_id
            )
            .scalar()
        )

        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "total_storage_bytes": int(
                total_storage or 0
            ),
        }


document_dashboard_service = DocumentDashboardService()