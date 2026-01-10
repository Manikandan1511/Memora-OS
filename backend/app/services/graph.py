# backend/app/services/graph.py

from app.db.neo4j import get_driver


def create_memory_node(memory: dict):
    driver = get_driver()

    query = """
    MERGE (m:Memory {id: $id})
    SET m.content = $content,
        m.source = $source,
        m.created_at = $created_at
    """

    with driver.session() as session:
        session.run(
            query,
            id=memory["id"],
            content=memory["content"],
            source=memory["source"],
            created_at=memory["created_at"]
        )


def link_related_memories(memory: dict):
    """
    Simple demo logic:
    Link new memory to all existing memories from same source
    """

    driver = get_driver()

    query = """
    MATCH (m:Memory {id: $id})
    MATCH (o:Memory)
    WHERE o.source = $source AND o.id <> $id
    MERGE (m)-[:RELATED_TO]->(o)
    """

    with driver.session() as session:
        session.run(
            query,
            id=memory["id"],
            source=memory["source"]
        )


def get_graph():
    driver = get_driver()

    query = """
    MATCH (a)-[r]->(b)
    RETURN a, r, b
    """

    nodes = {}
    edges = []

    with driver.session() as session:
        result = session.run(query)

        for record in result:
            a = record["a"]
            b = record["b"]
            r = record["r"]

            nodes[a["id"]] = {
                "id": a["id"],
                "content": a.get("content"),
                "source": a.get("source")
            }

            nodes[b["id"]] = {
                "id": b["id"],
                "content": b.get("content"),
                "source": b.get("source")
            }

            edges.append({
                "from": a["id"],
                "to": b["id"],
                "type": r.type
            })

    return {
        "nodes": list(nodes.values()),
        "edges": edges
    }
