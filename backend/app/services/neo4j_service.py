import hashlib
import re

from app.database.neo4j_database import neo4j_db
from app.schemas.graph import MemoryGraph


class Neo4jService:
    """Handles all interactions with the Neo4j database."""

    # =====================================================
    # Entity Normalization
    # =====================================================

    @staticmethod
    def normalize_entity_name(entity_name: str) -> str:
        """
        Normalize an entity name so that the same entity
        written with different spacing/capitalization can
        resolve to the same Neo4j entity node.
        """

        normalized = re.sub(
            r"\s+",
            " ",
            entity_name.strip(),
        )

        return normalized.lower()

    @classmethod
    def generate_entity_id(
        cls,
        entity_name: str,
        entity_type: str,
    ) -> str:
        """
        Generate a deterministic entity ID.

        The ID depends on the normalized entity name and
        entity type, not on the document ID.

        This allows the same entity to be shared across
        multiple documents.
        """

        normalized_name = cls.normalize_entity_name(
            entity_name
        )

        normalized_type = entity_type.strip().lower()

        entity_key = (
            f"{normalized_type}:{normalized_name}"
        )

        entity_hash = hashlib.sha256(
            entity_key.encode("utf-8")
        ).hexdigest()[:24]

        return f"entity_{entity_hash}"

    # =====================================================
    # Save Generic Memory Graph
    # =====================================================

    def save_graph(self, graph: MemoryGraph):

        with neo4j_db.get_session() as session:

            # ----------------------------
            # Create Nodes
            # ----------------------------

            for node in graph.nodes:

                session.run(
                    f"""
                    MERGE (n:{node.type.capitalize()} {{id: $id}})
                    SET n.name = $name
                    """,
                    id=node.id,
                    name=node.label,
                )

            # ----------------------------
            # Create Relationships
            # ----------------------------

            for edge in graph.edges:

                session.run(
                    """
                    MATCH (a {id: $source})
                    MATCH (b {id: $target})

                    MERGE (a)-[r:RELATED]->(b)

                    SET r.type = $relationship
                    """,
                    source=edge.source,
                    target=edge.target,
                    relationship=edge.relationship,
                )

    # =====================================================
    # F4 — Create User Node
    # =====================================================

    def create_user_node(
        self,
        user_id: int,
        name: str | None = None,
        email: str | None = None,
    ):
        """
        Create or reuse a User node.

        User nodes are shared across all memories and
        documents belonging to that user.
        """

        with neo4j_db.get_session() as session:

            session.run(
                """
                MERGE (u:User {id: $id})

                SET u.name = $name,
                    u.email = $email
                """,
                id=f"user_{user_id}",
                name=name,
                email=email,
            )

    # =====================================================
    # F4 — Create Memory Node
    # =====================================================

    def create_memory_node(
        self,
        memory_id: int,
        user_id: int,
        content: str,
        source: str | None = None,
    ):
        """
        Create or update a Memory node and connect it
        to its owning User.
        """

        with neo4j_db.get_session() as session:

            # ---------------------------------------------
            # Create / update Memory node
            # ---------------------------------------------

            session.run(
                """
                MERGE (m:Memory {id: $memory_id})

                SET m.user_id = $user_id,
                    m.content = $content,
                    m.source = $source
                """,
                memory_id=f"memory_{memory_id}",
                user_id=user_id,
                content=content,
                source=source,
            )

            # ---------------------------------------------
            # Connect User -> Memory
            # ---------------------------------------------

            session.run(
                """
                MERGE (u:User {id: $user_id})

                WITH u

                MATCH (m:Memory {id: $memory_id})

                MERGE (u)-[:HAS_MEMORY]->(m)
                """,
                user_id=f"user_{user_id}",
                memory_id=f"memory_{memory_id}",
            )

    # =====================================================
    # F4 — Link Memory -> Document
    # =====================================================

    def link_memory_to_document(
        self,
        memory_id: int,
        document_id: int,
    ):
        """
        Create the Memory -> Document relationship
        inside the unified knowledge graph.
        """

        with neo4j_db.get_session() as session:

            session.run(
                """
                MATCH (m:Memory {id: $memory_id})
                MATCH (d:Document {id: $document_id})

                MERGE (m)-[:REFERENCES_DOCUMENT]->(d)
                """,
                memory_id=f"memory_{memory_id}",
                document_id=f"document_{document_id}",
            )

    # =====================================================
    # Create Document Node
    # =====================================================

    def create_document_node(
        self,
        document_id: int,
        filename: str,
        category: str | None = None,
    ):

        with neo4j_db.get_session() as session:

            session.run(
                """
                MERGE (d:Document {id: $id})

                SET d.name = $name,
                    d.category = $category
                """,
                id=f"document_{document_id}",
                name=filename,
                category=category,
            )

    # =====================================================
    # Create / Link Document Entity Nodes
    # =====================================================

    def create_document_entities(
        self,
        document_id: int,
        entities: list,
    ):

        with neo4j_db.get_session() as session:

            document_node_id = f"document_{document_id}"

            for entity in entities:

                entity_text = entity.get(
                    "text",
                    "",
                ).strip()

                entity_label = entity.get(
                    "label",
                    "UNKNOWN",
                ).strip()

                if not entity_text:
                    continue

                # -------------------------------------------------
                # Generate a global deterministic entity ID.
                #
                # The document ID is NOT part of this ID.
                # -------------------------------------------------

                entity_id = self.generate_entity_id(
                    entity_name=entity_text,
                    entity_type=entity_label,
                )

                normalized_name = (
                    self.normalize_entity_name(
                        entity_text
                    )
                )

                # -------------------------------------------------
                # Create or reuse the shared Entity node.
                # -------------------------------------------------

                session.run(
                    """
                    MERGE (e:Entity {id: $entity_id})

                    SET e.name = $name,
                        e.normalized_name = $normalized_name,
                        e.type = $type
                    """,
                    entity_id=entity_id,
                    name=entity_text,
                    normalized_name=normalized_name,
                    type=entity_label,
                )

                # -------------------------------------------------
                # Connect Document -> Entity
                # -------------------------------------------------

                session.run(
                    """
                    MATCH (d:Document {id: $document_id})
                    MATCH (e:Entity {id: $entity_id})

                    MERGE (d)-[:CONTAINS_ENTITY]->(e)
                    """,
                    document_id=document_node_id,
                    entity_id=entity_id,
                )

    # =====================================================
    # Create Document Relationships
    # =====================================================

    def create_document_relationships(
        self,
        document_id: int,
        relationships: list,
    ):

        with neo4j_db.get_session() as session:

            document_node_id = f"document_{document_id}"

            for relationship in relationships:

                subject = relationship.get(
                    "subject",
                    "",
                ).strip()

                relationship_type = relationship.get(
                    "relationship",
                    "RELATED",
                ).strip()

                object_entity = relationship.get(
                    "object",
                    "",
                ).strip()

                if not subject or not object_entity:
                    continue

                # -------------------------------------------------
                # Find the shared subject entity through the
                # current document.
                # -------------------------------------------------

                result = session.run(
                    """
                    MATCH (d:Document {id: $document_id})
                    MATCH (d)-[:CONTAINS_ENTITY]->(e:Entity)
                    WHERE e.normalized_name = $entity_name
                    RETURN e.id AS id
                    LIMIT 1
                    """,
                    document_id=document_node_id,
                    entity_name=self.normalize_entity_name(
                        subject
                    ),
                ).single()

                subject_id = (
                    result["id"]
                    if result
                    else None
                )

                # -------------------------------------------------
                # Find the shared object entity through the
                # current document.
                # -------------------------------------------------

                result = session.run(
                    """
                    MATCH (d:Document {id: $document_id})
                    MATCH (d)-[:CONTAINS_ENTITY]->(e:Entity)
                    WHERE e.normalized_name = $entity_name
                    RETURN e.id AS id
                    LIMIT 1
                    """,
                    document_id=document_node_id,
                    entity_name=self.normalize_entity_name(
                        object_entity
                    ),
                ).single()

                object_id = (
                    result["id"]
                    if result
                    else None
                )

                if not subject_id or not object_id:
                    continue

                # -------------------------------------------------
                # Create the relationship between shared entities.
                # -------------------------------------------------

                session.run(
                    """
                    MATCH (a:Entity {id: $subject_id})
                    MATCH (b:Entity {id: $object_id})

                    MERGE (a)-[r:RELATED]->(b)

                    SET r.type = $relationship
                    """,
                    subject_id=subject_id,
                    object_id=object_id,
                    relationship=relationship_type,
                )

    # =====================================================
    # Migrate Existing F2 Entity Nodes
    # =====================================================

    def migrate_existing_entity_nodes(self):
        """
        Migrate old document-specific Entity nodes into the
        new globally shared Entity structure.

        Old format:

            entity_<document_id>_<index>

        New format:

            entity_<deterministic_hash>

        Existing document links and graph relationships are
        preserved.
        """

        with neo4j_db.get_session() as session:

            # -------------------------------------------------
            # Find all existing Entity nodes.
            # -------------------------------------------------

            result = session.run(
                """
                MATCH (e:Entity)
                RETURN e.id AS old_id,
                       e.name AS name,
                       e.type AS type
                ORDER BY e.id
                """
            )

            existing_entities = [
                {
                    "old_id": record["old_id"],
                    "name": record["name"],
                    "type": record["type"],
                }
                for record in result
            ]

            migrated_count = 0

            for entity in existing_entities:

                old_id = entity["old_id"]
                entity_name = (
                    entity["name"] or ""
                ).strip()

                entity_type = (
                    entity["type"] or "UNKNOWN"
                ).strip()

                if not entity_name:
                    continue

                # -------------------------------------------------
                # Generate the new shared entity ID.
                # -------------------------------------------------

                new_id = self.generate_entity_id(
                    entity_name=entity_name,
                    entity_type=entity_type,
                )

                normalized_name = (
                    self.normalize_entity_name(
                        entity_name
                    )
                )

                # -------------------------------------------------
                # Create/reuse the global Entity node.
                # -------------------------------------------------

                session.run(
                    """
                    MERGE (new_entity:Entity {id: $new_id})

                    SET new_entity.name = $name,
                        new_entity.normalized_name = $normalized_name,
                        new_entity.type = $type
                    """,
                    new_id=new_id,
                    name=entity_name,
                    normalized_name=normalized_name,
                    type=entity_type,
                )

                # -------------------------------------------------
                # Preserve Document -> Entity relationships.
                # -------------------------------------------------

                session.run(
                    """
                    MATCH (d:Document)-[:CONTAINS_ENTITY]->(old:Entity)
                    WHERE old.id = $old_id

                    MATCH (new_entity:Entity {id: $new_id})

                    MERGE (d)-[:CONTAINS_ENTITY]->(new_entity)
                    """,
                    old_id=old_id,
                    new_id=new_id,
                )

                # -------------------------------------------------
                # Preserve outgoing Entity relationships.
                # -------------------------------------------------

                session.run(
                    """
                    MATCH (old:Entity)-[r:RELATED]->(target:Entity)
                    WHERE old.id = $old_id

                    MATCH (new_entity:Entity {id: $new_id})

                    MERGE (new_entity)-[new_r:RELATED]->(target)

                    SET new_r.type = r.type
                    """,
                    old_id=old_id,
                    new_id=new_id,
                )

                # -------------------------------------------------
                # Preserve incoming Entity relationships.
                # -------------------------------------------------

                session.run(
                    """
                    MATCH (source:Entity)-[r:RELATED]->(old:Entity)
                    WHERE old.id = $old_id

                    MATCH (new_entity:Entity {id: $new_id})

                    MERGE (source)-[new_r:RELATED]->(new_entity)

                    SET new_r.type = r.type
                    """,
                    old_id=old_id,
                    new_id=new_id,
                )

                # -------------------------------------------------
                # Remove the old Entity node.
                # -------------------------------------------------

                if old_id != new_id:

                    session.run(
                        """
                        MATCH (old:Entity {id: $old_id})
                        DETACH DELETE old
                        """,
                        old_id=old_id,
                    )

                    migrated_count += 1

            return migrated_count


# =====================================================
# Singleton Service
# =====================================================

neo4j_service = Neo4jService()