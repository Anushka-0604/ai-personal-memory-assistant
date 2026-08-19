from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.memory import Memory
from app.database.neo4j_database import neo4j_db


class MemoryDocumentService:
    """
    Handles relationships between memories and documents.

    Also synchronizes memory-document relationships with Neo4j
    so the knowledge graph can represent:

        User -> Memory -> Document
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
    # Sync User -> Memory -> Document With Neo4j
    # =====================================================

    def _sync_memory_document_to_neo4j(
        self,
        memory: Memory,
        document: Document,
    ):
        """
        Create/update the unified Neo4j structure:

            User -> Memory -> Document

        The PostgreSQL database remains the source of truth.
        Neo4j stores the graph representation.
        """

        with neo4j_db.get_session() as session:

            # -------------------------------------------------
            # Create / reuse User node
            # -------------------------------------------------

            session.run(
                """
                MERGE (u:User {id: $user_id})

                SET u.user_id = $user_id
                """,
                user_id=f"user_{memory.user_id}",
            )

            # -------------------------------------------------
            # Create / reuse Memory node
            # -------------------------------------------------

            session.run(
                """
                MERGE (m:Memory {id: $memory_id})

                SET m.memory_id = $memory_id,
                    m.user_id = $user_id,
                    m.content = $content,
                    m.source = $source
                """,
                memory_id=f"memory_{memory.id}",
                user_id=f"user_{memory.user_id}",
                content=memory.content,
                source=memory.source,
            )

            # -------------------------------------------------
            # Create User -> Memory relationship
            # -------------------------------------------------

            session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (m:Memory {id: $memory_id})

                MERGE (u)-[:HAS_MEMORY]->(m)
                """,
                user_id=f"user_{memory.user_id}",
                memory_id=f"memory_{memory.id}",
            )

            # -------------------------------------------------
            # Ensure Document node exists
            # -------------------------------------------------

            session.run(
                """
                MERGE (d:Document {id: $document_id})

                SET d.name = $name,
                    d.category = $category
                """,
                document_id=f"document_{document.id}",
                name=document.original_filename,
                category=document.document_category,
            )

            # -------------------------------------------------
            # Create Memory -> Document relationship
            # -------------------------------------------------

            session.run(
                """
                MATCH (m:Memory {id: $memory_id})
                MATCH (d:Document {id: $document_id})

                MERGE (m)-[:REFERENCES_DOCUMENT]->(d)
                """,
                memory_id=f"memory_{memory.id}",
                document_id=f"document_{document.id}",
            )

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

        The relationship is stored in PostgreSQL and
        synchronized with Neo4j.
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

        # -------------------------------------------------
        # Synchronize with Neo4j
        # -------------------------------------------------

        self._sync_memory_document_to_neo4j(
            memory=memory,
            document=document,
        )

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

        # -------------------------------------------------
        # Remove only the Memory -> Document relationship
        # -------------------------------------------------

        with neo4j_db.get_session() as session:

            session.run(
                """
                MATCH (m:Memory {id: $memory_id})
                MATCH (d:Document {id: $document_id})

                MATCH (m)-[r:REFERENCES_DOCUMENT]->(d)

                DELETE r
                """,
                memory_id=f"memory_{memory.id}",
                document_id=f"document_{document.id}",
            )

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