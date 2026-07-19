from app.database.neo4j_database import neo4j_db


class GraphQueryService:
    """Provides methods for querying the Neo4j knowledge graph."""

    def get_people(self):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (p:Person)
                RETURN p.name AS name
                ORDER BY name
                """
            )

            return [record["name"] for record in result]

    def get_organizations(self):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (o:Organization)
                RETURN o.name AS name
                ORDER BY name
                """
            )

            return [record["name"] for record in result]

    def get_locations(self):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (l:Location)
                RETURN l.name AS name
                ORDER BY name
                """
            )

            return [record["name"] for record in result]

    def get_organizations_for_person(self, person_name: str):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (p:Person)-[r]->(o:Organization)
                WHERE p.name = $name
                RETURN o.name AS organization
                ORDER BY organization
                """,
                name=person_name,
            )

            return [record["organization"] for record in result]

    def get_people_for_organization(self, organization_name: str):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (p:Person)-[r]->(o:Organization)
                WHERE o.name = $name
                RETURN p.name AS person
                ORDER BY person
                """,
                name=organization_name,
            )

            return [record["person"] for record in result]

    def get_locations_for_person(self, person_name: str):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (p:Person)-[r]->(l:Location)
                WHERE p.name = $name
                RETURN l.name AS location
                ORDER BY location
                """,
                name=person_name,
            )

            return [record["location"] for record in result]

    def get_people_for_location(self, location_name: str):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (p:Person)-[r]->(l:Location)
                WHERE l.name = $name
                RETURN p.name AS person
                ORDER BY person
                """,
                name=location_name,
            )

            return [record["person"] for record in result]

    def get_locations_for_organization(self, organization_name: str):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (p:Person)-[:RELATED]->(o:Organization)
                MATCH (p)-[:RELATED]->(l:Location)
                WHERE o.name = $name
                RETURN DISTINCT l.name AS location
                ORDER BY location
                """,
                name=organization_name,
            )

            return [record["location"] for record in result]

    def get_organizations_for_location(self, location_name: str):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (p:Person)-[:RELATED]->(l:Location)
                MATCH (p)-[:RELATED]->(o:Organization)
                WHERE l.name = $name
                RETURN DISTINCT o.name AS organization
                ORDER BY organization
                """,
                name=location_name,
            )

            return [record["organization"] for record in result]


graph_query_service = GraphQueryService()