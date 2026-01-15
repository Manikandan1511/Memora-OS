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

def expand_context_from_memories(memory_ids: list, limit: int = 5):
    """
    Expand reasoning context using Neo4j relationships.
    Used by AskBrain.
    """
    if not memory_ids:
        return []

    driver = get_driver()

    query = """
    MATCH (m:Memory)-[r]->(related:Memory)
    WHERE m.id IN $memory_ids
    RETURN DISTINCT related.content AS content, type(r) AS relation
    LIMIT $limit
    """

    expanded = []

    with driver.session() as session:
        results = session.run(
            query,
            memory_ids=memory_ids,
            limit=limit
        )

        for record in results:
            expanded.append({
                "content": record["content"],
                "relation": record["relation"]
            })

    return expanded

def get_memory_timeline(limit: int = 20):
    """
    Fetch memories ordered by time for timeline-aware reasoning.
    """
    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE m.created_at IS NOT NULL
    RETURN m.content AS content, m.created_at AS created_at
    ORDER BY m.created_at ASC
    LIMIT $limit
    """

    timeline = []

    with driver.session() as session:
        results = session.run(query, limit=limit)

        for record in results:
            timeline.append({
                "content": record["content"],
                "created_at": record["created_at"]
            })

    return timeline
