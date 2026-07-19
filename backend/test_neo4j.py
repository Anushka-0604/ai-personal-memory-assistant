from app.database.neo4j_database import neo4j_db

with neo4j_db.get_session() as session:

    session.run(
        """
        CREATE (p:Person {
            name: $name
        })
        """,
        name="Alice",
    )

    print("Person node created successfully!")

neo4j_db.close()