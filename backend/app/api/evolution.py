# backend/app/api/evolution.py

from fastapi import APIRouter
from app.db.neo4j import get_driver

router = APIRouter(prefix="/api/v1/evolution", tags=["Evolution"])


@router.get("/{memory_id}")
def get_memory_evolution(memory_id: str):
    driver = get_driver()

    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Memory {id: $id})-[r]->(b:Memory)
            RETURN type(r) AS relation,
                   b.id AS id,
                   b.content AS content
            """,
            id=memory_id
        )

        evolution = []
        for record in result:
            evolution.append({
                "relation": record["relation"],
                "id": record["id"],
                "content": record["content"]
            })

    return {"evolution": evolution}
