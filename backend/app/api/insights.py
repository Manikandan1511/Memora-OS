from fastapi import APIRouter
from app.db.neo4j import get_driver

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/dashboard")
def get_dashboard_stats():
    driver = get_driver()

    query = """
    MATCH (m:Memory)
    RETURN 
        count(m) AS total,
        sum(CASE WHEN m.archived = true THEN 1 ELSE 0 END) AS archived,
        sum(CASE WHEN m.archived = false THEN 1 ELSE 0 END) AS active,
        sum(CASE WHEN m.strength >= 0.7 THEN 1 ELSE 0 END) AS strong,
        sum(CASE WHEN m.strength >= 0.4 AND m.strength < 0.7 THEN 1 ELSE 0 END) AS weak,
        sum(CASE WHEN m.strength < 0.4 THEN 1 ELSE 0 END) AS fading
    """

    rel_query = """
    MATCH ()-[r]->()
    RETURN count(r) AS connections
    """

    with driver.session() as session:
        stats = session.run(query).single()
        rels = session.run(rel_query).single()

    return {
        "total_memories": stats["total"],
        "active_memories": stats["active"],
        "archived_memories": stats["archived"],
        "strong_memories": stats["strong"],
        "weak_memories": stats["weak"],
        "fading_memories": stats["fading"],
        "connections": rels["connections"],
    }