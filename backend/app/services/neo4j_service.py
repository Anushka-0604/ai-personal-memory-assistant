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
                # IMPORTANT:
                # The document ID is NOT part of this ID.
                #
                # Therefore:
                #
                # Document 12 -> Process
                # Document 13 -> Process
                #
                # both resolve to the same Entity node.
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
                # Find the shared entity nodes through the current
                # document.
                #
                # Because entities are now globally shared,
                # this can connect entities that also appear in
                # other documents.
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
                # Create the relationship between the shared
                # entity nodes.
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
# Singleton Service
# =====================================================

neo4j_service = Neo4jService()