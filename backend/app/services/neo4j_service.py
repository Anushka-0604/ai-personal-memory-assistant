from app.database.neo4j_database import neo4j_db
from app.schemas.graph import MemoryGraph


class Neo4jService:
    """Handles all interactions with the Neo4j database."""

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
    # Create Document Entity Nodes
    # =====================================================

    def create_document_entities(
        self,
        document_id: int,
        entities: list,
    ):

        with neo4j_db.get_session() as session:

            document_node_id = f"document_{document_id}"

            for index, entity in enumerate(entities):

                entity_text = entity.get("text", "").strip()
                entity_label = entity.get("label", "UNKNOWN")

                if not entity_text:
                    continue

                # Create a stable unique ID for the entity
                entity_id = (
                    f"entity_{document_id}_{index}"
                )

                # Create Entity node
                session.run(
                    """
                    MERGE (e:Entity {id: $entity_id})

                    SET e.name = $name,
                        e.type = $type
                    """,
                    entity_id=entity_id,
                    name=entity_text,
                    type=entity_label,
                )

                # Connect Document -> Entity
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
# Singleton Service
# =====================================================

neo4j_service = Neo4jService()