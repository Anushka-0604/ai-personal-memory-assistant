from app.database.neo4j_database import neo4j_db


class GraphQueryService:
    """Provides methods to query the Neo4j knowledge graph."""

    # =====================================================
    # People
    # =====================================================

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

    # =====================================================
    # Organizations
    # =====================================================

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

    # =====================================================
    # Locations
    # =====================================================

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

    # =====================================================
    # Person -> Organization
    # =====================================================

    def get_organizations_for_person(
        self,
        person_name: str,
    ):
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

            return [
                record["organization"]
                for record in result
            ]

    # =====================================================
    # Organization -> People
    # =====================================================

    def get_people_for_organization(
        self,
        organization_name: str,
    ):
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

            return [
                record["person"]
                for record in result
            ]

    # =====================================================
    # Person -> Location
    # =====================================================

    def get_locations_for_person(
        self,
        person_name: str,
    ):
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

            return [
                record["location"]
                for record in result
            ]

    # =====================================================
    # Location -> People
    # =====================================================

    def get_people_for_location(
        self,
        location_name: str,
    ):
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

            return [
                record["person"]
                for record in result
            ]

    # =====================================================
    # Organization -> Locations
    # =====================================================

    def get_locations_for_organization(
        self,
        organization_name: str,
    ):
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

            return [
                record["location"]
                for record in result
            ]

    # =====================================================
    # Location -> Organizations
    # =====================================================

    def get_organizations_for_location(
        self,
        location_name: str,
    ):
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

            return [
                record["organization"]
                for record in result
            ]

    # =====================================================
    # Document Graph Queries
    # =====================================================

    def get_document_entities(
        self,
        document_id: int,
    ):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (d:Document {id: $document_id})
                      -[:CONTAINS_ENTITY]->(e:Entity)

                RETURN e.name AS name,
                       e.type AS type

                ORDER BY name
                """,
                document_id=f"document_{document_id}",
            )

            return [
                {
                    "name": record["name"],
                    "type": record["type"],
                }
                for record in result
            ]

    # =====================================================
    # Document Relationships
    # =====================================================

    def get_document_relationships(
        self,
        document_id: int,
    ):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (d:Document {id: $document_id})
                      -[:CONTAINS_ENTITY]->(a:Entity)
                      -[r:RELATED]->(b:Entity)

                RETURN a.name AS subject,
                       r.type AS relationship,
                       b.name AS object

                ORDER BY subject, relationship, object
                """,
                document_id=f"document_{document_id}",
            )

            return [
                {
                    "subject": record["subject"],
                    "relationship": record["relationship"],
                    "object": record["object"],
                }
                for record in result
            ]

    # =====================================================
    # Entity Connection Queries
    # =====================================================

    def get_entity_connections(
        self,
        entity_name: str,
    ):
        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (a:Entity)-[r:RELATED]->(b:Entity)

                WHERE toLower(a.name) = toLower($entity_name)

                RETURN b.name AS entity,
                       r.type AS relationship

                ORDER BY entity
                """,
                entity_name=entity_name,
            )

            return [
                {
                    "entity": record["entity"],
                    "relationship": record["relationship"],
                }
                for record in result
            ]

    # =====================================================
    # F3 — Cross-Document Relationships
    # =====================================================

    def get_cross_document_relationships(
        self,
        entity_name: str,
    ):
        """
        Find relationships for an entity that is shared
        across multiple documents.

        The entity itself is globally shared through a
        deterministic Entity ID.

        A relationship is returned together with the
        documents in which the subject entity appears.

        The object entity does not have to appear in the
        target document for the relationship to be valid.
        """

        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (subject:Entity)-[r:RELATED]->(object:Entity)

                WHERE toLower(subject.name) =
                      toLower($entity_name)

                MATCH (source_document:Document)
                      -[:CONTAINS_ENTITY]->
                      (subject)

                OPTIONAL MATCH (target_document:Document)
                      -[:CONTAINS_ENTITY]->
                      (object)

                RETURN DISTINCT
                       subject.name AS subject,
                       subject.type AS subject_type,
                       r.type AS relationship,
                       object.name AS object,
                       object.type AS object_type,
                       collect(DISTINCT source_document.name)
                           AS source_documents,
                       collect(DISTINCT target_document.name)
                           AS target_documents

                ORDER BY
                    subject,
                    relationship,
                    object
                """,
                entity_name=entity_name,
            )

            return [
                {
                    "subject": record["subject"],
                    "subject_type": record["subject_type"],
                    "relationship": record["relationship"],
                    "object": record["object"],
                    "object_type": record["object_type"],
                    "source_documents": record[
                        "source_documents"
                    ],
                    "target_documents": [
                        document
                        for document in record[
                            "target_documents"
                        ]
                        if document is not None
                    ],
                }
                for record in result
            ]

    # =====================================================
    # Multi-Hop Graph Traversal
    # =====================================================

    def get_entity_connections_by_depth(
        self,
        entity_name: str,
        depth: int = 2,
    ):
        if depth < 1:
            depth = 1

        if depth > 5:
            depth = 5

        with neo4j_db.get_session() as session:

            query = f"""
                MATCH path =
                    (start:Entity)-[:RELATED*1..{depth}]->(target:Entity)

                WHERE toLower(start.name) =
                      toLower($entity_name)

                RETURN DISTINCT
                    target.name AS entity,
                    length(path) AS distance

                ORDER BY distance, entity
            """

            result = session.run(
                query,
                entity_name=entity_name,
            )

            return [
                {
                    "entity": record["entity"],
                    "distance": record["distance"],
                }
                for record in result
            ]


# =====================================================
# Singleton Service
# =====================================================

graph_query_service = GraphQueryService()