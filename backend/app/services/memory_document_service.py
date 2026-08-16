from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.memory import Memory


class MemoryDocumentService:
    """
    Handles relationships between memories and documents.
    """

    # =====================================================
    # Get Memory And Document For User
    # =====================================================

    def _get_memory_and_document(
        self,
        db: Session,
        memory_id: int,
        document_id: int,
        user_id: int,
    ):
        """
        Retrieve a memory and document only when both belong
        to the current user.
        """

        memory = (
            db.query(Memory)
            .filter(
                Memory.id == memory_id,
                Memory.user_id == user_id,
            )
            .first()
        )

        if memory is None:
            raise ValueError(
                "Memory not found."
            )

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id,
                Document.user_id == user_id,
            )
            .first()
        )

        if document is None:
            raise ValueError(
                "Document not found."
            )

        return memory, document

    # =====================================================
    # Link Memory -> Document
    # =====================================================

    def link_memory_to_document(
        self,
        db: Session,
        memory_id: int,
        document_id: int,
        user_id: int,
    ) -> bool:
        """
        Link a user's memory to one of their documents.
        """

        memory, document = (
            self._get_memory_and_document(
                db=db,
                memory_id=memory_id,
                document_id=document_id,
                user_id=user_id,
            )
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
        user_id: int,
    ) -> bool:
        """
        Remove the relationship between a user's memory
        and document.
        """

        memory, document = (
            self._get_memory_and_document(
                db=db,
                memory_id=memory_id,
                document_id=document_id,
                user_id=user_id,
            )
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
        user_id: int,
    ) -> list[Document]:
        """
        Return documents linked to a memory belonging
        to the current user.
        """

        memory = (
            db.query(Memory)
            .filter(
                Memory.id == memory_id,
                Memory.user_id == user_id,
            )
            .first()
        )

        if memory is None:
            raise ValueError(
                "Memory not found."
            )

        return memory.documents

    # =====================================================
    # Get Memories For Document
    # =====================================================

    def get_memories_for_document(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ) -> list[Memory]:
        """
        Return memories linked to a document belonging
        to the current user.
        """

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id,
                Document.user_id == user_id,
            )
            .first()
        )

        if document is None:
            raise ValueError(
                "Document not found."
            )

        return document.memories


# =====================================================
# Singleton Service
# =====================================================

memory_document_service = MemoryDocumentService()