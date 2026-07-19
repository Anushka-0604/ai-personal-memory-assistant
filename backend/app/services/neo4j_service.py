from app.database.neo4j_database import neo4j_db
from app.schemas.graph import MemoryGraph


class Neo4jService:
    """Handles all interactions with the Neo4j database."""

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


neo4j_service = Neo4jService()