# backend/app/services/evolution.py

from app.db.chroma import get_collection
from app.db.neo4j import get_driver


TOP_K = 3


def evolve_memory(new_memory_id: str, new_embedding: list[float]) -> None:
    """
    Always link new memory to top-k existing memories.
    Safe demo mode: guarantees evolution graph growth.
    """

    collection = get_collection()

    # Query top-k similar memories from Chroma
    results = collection.query(
        query_embeddings=[new_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas"]
    )

    metadatas = results.get("metadatas", [[]])[0]

    if not metadatas:
        return

    driver = get_driver()

    with driver.session() as session:
        for meta in metadatas:
            existing_id = meta.get("id")

            if not existing_id:
                continue

            if existing_id == new_memory_id:
                continue 

            # Create relationship in Neo4j
            session.run(
                """
                MATCH (a:Memory {id: $new_id})
                MATCH (b:Memory {id: $existing_id})
                MERGE (a)-[:RELATED_TO]->(b)
                """,
                new_id=new_memory_id,
                existing_id=existing_id
            )
