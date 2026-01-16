# backend/app/services/graph.py

from datetime import datetime, timezone
from app.db.neo4j import get_driver
from app.services.forgetting import apply_time_decay


# WRITE OPERATIONS

def create_memory_node(memory: dict):
    """
    Create or update a memory node in Neo4j.
    Always stores UTC-aware datetime.
    """
    driver = get_driver()

    created_at = memory.get("created_at")

    #  Normalize created_at to UTC-aware datetime
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    query = """
    MERGE (m:Memory {id: $id})
    SET m.content = $content,
        m.source = $source,
        m.created_at = $created_at,
        m.strength = $strength
    """

    with driver.session() as session:
        session.run(
            query,
            id=memory["id"],
            content=memory["content"],
            source=memory["source"],
            created_at=created_at,
            strength=memory.get("strength", 0.8)
        )


def link_related_memories(memory: dict):
    """
    Link new memory to existing memories from the same source.
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


# READ OPERATIONS

def get_graph():
    """
    Return full knowledge graph (nodes + edges).
    Used by Brain Graph frontend.
    """
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


def get_memory_timeline(limit: int = 50):
    """
    Timeline with time-decay aware strength.
    Handles Neo4j DateTime, ISO strings, and UTC safely.
    """
    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE m.created_at IS NOT NULL
    RETURN m.content AS content,
           m.created_at AS created_at,
           coalesce(m.strength, 0.8) AS strength
    ORDER BY m.created_at ASC
    LIMIT $limit
    """

    timeline = []

    with driver.session() as session:
        results = session.run(query, limit=limit)

        for record in results:
            created_at = record["created_at"]
            base_strength = record["strength"]

            #  Convert Neo4j / string → Python datetime
            if isinstance(created_at, str):
                created_at_dt = datetime.fromisoformat(created_at)
            else:
                created_at_dt = created_at.to_native()

            #  FORCE UTC AWARENESS
            if created_at_dt.tzinfo is None:
                created_at_dt = created_at_dt.replace(tzinfo=timezone.utc)

            #  Apply forgetting safely
            decayed_strength = apply_time_decay(
                created_at_dt,
                base_strength
            )

            timeline.append({
                "content": record["content"],
                "created_at": created_at_dt.isoformat(),
                "strength": round(decayed_strength, 2),
                "state": (
                    "strong" if decayed_strength > 0.7 else
                    "weak" if decayed_strength > 0.3 else
                    "fading"
                )
            })

    return timeline
