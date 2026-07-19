from neo4j import GraphDatabase

from app.core.config import (
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USERNAME,
)


class Neo4jDatabase:
    """Manages the Neo4j database connection."""

    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        )

    def close(self):
        self.driver.close()

    def get_session(self):
        return self.driver.session()


neo4j_db = Neo4jDatabase()