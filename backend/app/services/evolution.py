# backend/app/services/evolution.py

from app.db.neo4j import get_driver

def decide_relation(new_content: str, old_content: str) -> str:
    """
    Simple deterministic evolution rules.
    Stable and explainable.
    """

    new_text = new_content.lower()
    old_text = old_content.lower()

    if any(word in new_text for word in ["but", "however", "incorrect", "wrong"]):
        return "CONTRADICTS"

    if len(new_text) > len(old_text):
        return "EVOLVES_TO"

    return "REFINES"


def evolve_memory(new_memory_id: str, new_content: str):
    """
    Create evolution relationships from older memories
    to the newly added memory.
    """

    driver = get_driver()

    with driver.session() as session:
        existing = session.run(
            """
            MATCH (m:Memory)
            WHERE m.id <> $new_id
            RETURN m.id AS id, m.content AS content
            """,
            new_id=new_memory_id
        )

        for record in existing:
            relation = decide_relation(
                new_content=new_content,
                old_content=record["content"]
            )

            session.run(
                f"""
                MATCH (old:Memory {{id: $old_id}})
                MATCH (new:Memory {{id: $new_id}})
                MERGE (old)-[r:{relation}]->(new)
                """,
                old_id=record["id"],
                new_id=new_memory_id
            )
