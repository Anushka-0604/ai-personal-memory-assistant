from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.memory import Memory


class MemoryDocumentService:
    """
    Handles relationships between memories and documents.
    """

    # =====================================================
    # Link Memory -> Document
    # =====================================================

    def link_memory_to_document(
        self,
        db: Session,
        memory_id: int,
        document_id: int,
    ) -> bool:
        """
        Link an existing memory to an existing document.

        Returns True if the relationship exists after the
        operation.
        """

        memory = (
            db.query(Memory)
            .filter(Memory.id == memory_id)
            .first()
        )

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if memory is None:
            raise ValueError(
                f"Memory {memory_id} not found."
            )

        if document is None:
            raise ValueError(
                f"Document {document_id} not found."
            )

        if document not in memory.documents:
            memory.documents.append(document)

            db.commit()
            db.refresh(memory)

        return True

    # =====================================================
    # Unlink Memory -> Document
    # =====================================================

    def unlink_memory_from_document(
        self,
        db: Session,
        memory_id: int,
        document_id: int,
    ) -> bool:
        """
        Remove the relationship between a memory and
        a document.
        """

        memory = (
            db.query(Memory)
            .filter(Memory.id == memory_id)
            .first()
        )

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if memory is None:
            raise ValueError(
                f"Memory {memory_id} not found."
            )

        if document is None:
            raise ValueError(
                f"Document {document_id} not found."
            )

        if document in memory.documents:
            memory.documents.remove(document)

            db.commit()
            db.refresh(memory)

        return True

    # =====================================================
    # Get Documents For Memory
    # =====================================================

    def get_documents_for_memory(
        self,
        db: Session,
        memory_id: int,
    ) -> list[Document]:
        """
        Return all documents linked to a memory.
        """

        memory = (
            db.query(Memory)
            .filter(Memory.id == memory_id)
            .first()
        )

        if memory is None:
            raise ValueError(
                f"Memory {memory_id} not found."
            )

        return memory.documents

    # =====================================================
    # Get Memories For Document
    # =====================================================

    def get_memories_for_document(
        self,
        db: Session,
        document_id: int,
    ) -> list[Memory]:
        """
        Return all memories linked to a document.
        """

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise ValueError(
                f"Document {document_id} not found."
            )

        return document.memories


# =====================================================
# Singleton Service
# =====================================================

memory_document_service = MemoryDocumentService()