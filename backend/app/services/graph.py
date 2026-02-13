# backend/app/services/graph.py

from datetime import datetime, timezone
from typing import List
from app.db.neo4j import get_driver
from app.services.forgetting import apply_time_decay


def create_memory_node(memory: dict):
    """
    Create or update a memory node in Neo4j.
    Always stores UTC-aware datetime.
    """

    driver = get_driver()

    created_at = memory.get("created_at")

    # Normalize created_at safely
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    query = """
    MERGE (m:Memory {id: $id})
    SET m.content = $content,
        m.source = $source,
        m.created_at = $created_at,
        m.strength = coalesce(m.strength, $strength),
        m.archived = coalesce(m.archived, false)
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
    Link new memory to existing memories from same source.
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

# DECAY ENGINE 

def run_decay_cycle(threshold: float = 0.3):
    """
    Applies real decay to all non-archived memories.
    Updates stored strength.
    Archives memories below threshold.
    SAFE: does NOT delete anything.
    """

    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE coalesce(m.archived, false) = false
      AND m.created_at IS NOT NULL
    RETURN m.id AS id,
           m.created_at AS created_at,
           coalesce(m.strength, 0.8) AS strength
    """

    with driver.session() as session:
        results = session.run(query)

        for record in results:
            memory_id = record["id"]
            created_at = record["created_at"]
            base_strength = record["strength"]

            # Convert Neo4j datetime or ISO string
            if isinstance(created_at, str):
                created_at_dt = datetime.fromisoformat(created_at)
            else:
                created_at_dt = created_at.to_native()

            # Force UTC awareness
            if created_at_dt.tzinfo is None:
                created_at_dt = created_at_dt.replace(tzinfo=timezone.utc)

            decayed_strength = apply_time_decay(
                created_at_dt,
                base_strength
            )

            session.run(
                """
                MATCH (m:Memory {id: $id})
                SET m.strength = $strength,
                    m.archived = CASE
                        WHEN $strength <= $threshold THEN true
                        ELSE false
                    END
                """,
                id=memory_id,
                strength=round(decayed_strength, 4),
                threshold=threshold
            )



def get_graph():
    """
    Return full knowledge graph (nodes + edges).
    """

    driver = get_driver()

    query = """
    MATCH (a)-[r]->(b)
    RETURN a, r, b
    """

    nodes = {}
    edges = []

    with driver.session() as session:
        results = session.run(query)

        for record in results:
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


def expand_context_from_memories(memory_ids: List[str], limit: int = 5):
    """
    Expand reasoning context using Neo4j relationships.
    Ignores archived memories.
    """

    if not memory_ids:
        return []

    driver = get_driver()

    query = """
    MATCH (m:Memory)-[r]->(related:Memory)
    WHERE m.id IN $memory_ids
      AND coalesce(related.archived, false) = false
    RETURN DISTINCT related.content AS content,
           type(r) AS relation
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

def get_memory_timeline(limit: int = 100):
    """
    Timeline with full cognitive state.
    Returns ALL memories including archived ones.
    Sorted newest first.
    """

    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE m.created_at IS NOT NULL
    RETURN m.content AS content,
           m.created_at AS created_at,
           coalesce(m.strength, 0.8) AS strength,
           coalesce(m.archived, false) AS archived
    ORDER BY m.created_at DESC
    LIMIT $limit
    """

    timeline = []

    with driver.session() as session:
        results = session.run(query, limit=limit)

        for record in results:
            created_at = record["created_at"]
            base_strength = record["strength"]
            archived = record["archived"]

            # Convert to Python datetime safely
            if isinstance(created_at, str):
                created_at_dt = datetime.fromisoformat(created_at)
            else:
                created_at_dt = created_at.to_native()

            if created_at_dt.tzinfo is None:
                created_at_dt = created_at_dt.replace(tzinfo=timezone.utc)

            # Apply decay
            decayed_strength = apply_time_decay(
                created_at_dt,
                base_strength
            )

            # Determine cognitive state
            if archived:
                state = "archived"
            elif decayed_strength >= 0.7:
                state = "strong"
            elif decayed_strength >= 0.4:
                state = "weak"
            else:
                state = "fading"

            timeline.append({
                "content": record["content"],
                "created_at": created_at_dt.isoformat(),
                "strength": round(decayed_strength, 2),
                "archived": archived,
                "state": state
            })

    return timeline


# REINFORCEMENT

def reinforce_memories(memory_ids: List[str], boost: float = 0.05):
    """
    Increase strength of recalled memories.
    Safe: only updates strength.
    """

    if not memory_ids:
        return

    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE m.id IN $memory_ids
    SET m.strength =
        CASE
            WHEN m.strength IS NULL THEN $boost
            WHEN m.strength + $boost > 1.0 THEN 1.0
            ELSE m.strength + $boost
        END
    """

    with driver.session() as session:
        session.run(
            query,
            memory_ids=memory_ids,
            boost=boost
        )


def archive_faded_memories(threshold: float = 0.3):
    """
    Manually archive memories below threshold.
    Safe: does NOT delete anything.
    """

    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE coalesce(m.strength, 0.8) <= $threshold
    SET m.archived = true
    """

    with driver.session() as session:
        session.run(query, threshold=threshold)
