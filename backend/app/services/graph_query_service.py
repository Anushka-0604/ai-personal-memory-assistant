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

                RETURN
                    b.name AS entity,
                    "OUTGOING" AS direction,
                    r.type AS relationship

                UNION

                MATCH (a:Entity)-[r:RELATED]->(b:Entity)

                WHERE toLower(b.name) = toLower($entity_name)

                RETURN
                    a.name AS entity,
                    "INCOMING" AS direction,
                    r.type AS relationship

                ORDER BY entity
                """,
                entity_name=entity_name,
            )

            return [
                {
                    "entity": record["entity"],
                    "direction": record["direction"],
                    "relationship": record["relationship"],
                }
                for record in result
            ]

    # =====================================================
    # Cross-Document Relationships
    # =====================================================

    def get_cross_document_relationships(
        self,
        entity_name: str,
    ):
        """
        Find relationships involving an entity that is shared
        across multiple documents.
        """

        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (source_document:Document)
                      -[:CONTAINS_ENTITY]->
                      (subject:Entity)
                      -[r:RELATED]->
                      (object:Entity)
                      <-[:CONTAINS_ENTITY]-
                      (target_document:Document)

                WHERE toLower(subject.name) =
                      toLower($entity_name)

                RETURN DISTINCT
                       subject.name AS subject,
                       subject.type AS subject_type,
                       r.type AS relationship,
                       object.name AS object,
                       object.type AS object_type,
                       source_document.name AS source_document,
                       target_document.name AS target_document

                ORDER BY
                    subject,
                    relationship,
                    object,
                    source_document,
                    target_document
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
                    "source_document": record["source_document"],
                    "target_document": record["target_document"],
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
    # F5 — Documents For Memory
    # =====================================================

    def get_documents_for_memory(
        self,
        memory_id: int,
    ):
        """
        Retrieve documents connected to a memory through
        the Neo4j knowledge graph.

        Graph path:

            Memory -> REFERENCES_DOCUMENT -> Document
        """

        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (m:Memory {id: $memory_id})
                      -[:REFERENCES_DOCUMENT]->
                      (d:Document)

                RETURN
                    d.id AS document_id,
                    d.name AS document_name,
                    d.category AS category

                ORDER BY document_name
                """,
                memory_id=f"memory_{memory_id}",
            )

            return [
                {
                    "document_id": record["document_id"],
                    "document_name": record["document_name"],
                    "category": record["category"],
                }
                for record in result
            ]

    # =====================================================
    # F5 — Memories For Document
    # =====================================================

    def get_memories_for_document(
        self,
        document_id: int,
    ):
        """
        Retrieve memories connected to a document through
        the Neo4j knowledge graph.

        Graph path:

            Memory -> REFERENCES_DOCUMENT -> Document
        """

        with neo4j_db.get_session() as session:

            result = session.run(
                """
                MATCH (m:Memory)-[:REFERENCES_DOCUMENT]->
                      (d:Document {id: $document_id})

                RETURN
                    m.id AS memory_id,
                    m.content AS memory_content,
                    m.user_id AS user_id

                ORDER BY memory_id
                """,
                document_id=f"document_{document_id}",
            )

            return [
                {
                    "memory_id": record["memory_id"],
                    "memory_content": record["memory_content"],
                    "user_id": record["user_id"],
                }
                for record in result
            ]


# =====================================================
# Singleton
# =====================================================

graph_query_service = GraphQueryService()