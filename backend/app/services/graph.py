# backend/app/services/graph.py

from datetime import datetime, timezone
from typing import List
from app.db.neo4j import get_driver
from app.services.forgetting import apply_time_decay


# CREATE MEMORY NODE

def create_memory_node(memory: dict):
    driver = get_driver()

    created_at = memory.get("created_at")

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

# LINK MEMORIES

def link_related_memories(memory: dict):
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
    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE coalesce(m.archived, false) = false
      AND m.created_at IS NOT NULL
    RETURN m.id AS id,
           m.created_at AS created_at,
           m.last_accessed AS last_accessed,
           coalesce(m.strength, 0.8) AS strength
    """

    with driver.session() as session:
        results = session.run(query)

        for record in results:
            memory_id = record["id"]
            base_strength = record["strength"]

            # 🔥 USE last_accessed IF EXISTS
            last_accessed = record.get("last_accessed")

            if last_accessed:
                if isinstance(last_accessed, str):
                    base_time = datetime.fromisoformat(last_accessed)
                else:
                    base_time = last_accessed.to_native()
            else:
                created_at = record["created_at"]
                if isinstance(created_at, str):
                    base_time = datetime.fromisoformat(created_at)
                else:
                    base_time = created_at.to_native()

            if base_time.tzinfo is None:
                base_time = base_time.replace(tzinfo=timezone.utc)

            decayed_strength = apply_time_decay(
                base_time,
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

# GRAPH FETCH

def get_graph():
    """
    Returns full graph with cognitive state (strength + archived + state)
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

            # NODE A
            if a["id"] not in nodes:
                strength = a.get("strength", 0.8)
                archived = a.get("archived", False)

                # 🧠 Determine state
                if archived:
                    state = "archived"
                elif strength >= 0.7:
                    state = "strong"
                elif strength >= 0.4:
                    state = "weak"
                else:
                    state = "fading"

                nodes[a["id"]] = {
                    "id": a["id"],
                    "content": a.get("content"),
                    "source": a.get("source"),
                    "strength": strength,
                    "archived": archived,
                    "state": state
                }

            # NODE B
            if b["id"] not in nodes:
                strength = b.get("strength", 0.8)
                archived = b.get("archived", False)

                # 🧠 Determine state
                if archived:
                    state = "archived"
                elif strength >= 0.7:
                    state = "strong"
                elif strength >= 0.4:
                    state = "weak"
                else:
                    state = "fading"

                nodes[b["id"]] = {
                    "id": b["id"],
                    "content": b.get("content"),
                    "source": b.get("source"),
                    "strength": strength,
                    "archived": archived,
                    "state": state
                }

            # EDGE 
            edges.append({
                "from": a["id"],
                "to": b["id"],
                "type": r.type
            })

    return {
        "nodes": list(nodes.values()),
        "edges": edges
    }

# GRAPH CONTEXT

def expand_context_from_memories(memory_ids: List[str], limit: int = 5):
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


# TIMELINE

def get_memory_timeline(limit: int = 100):
    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE m.created_at IS NOT NULL
    RETURN m.content AS content,
           m.created_at AS created_at,
           m.last_accessed AS last_accessed,
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
            last_accessed = record.get("last_accessed")

            # Convert created_at
            if isinstance(created_at, str):
                created_at_dt = datetime.fromisoformat(created_at)
            else:
                created_at_dt = created_at.to_native()

            if created_at_dt.tzinfo is None:
                created_at_dt = created_at_dt.replace(tzinfo=timezone.utc)

            # 🔥 USE last_accessed FOR DECAY
            if last_accessed:
                if isinstance(last_accessed, str):
                    base_time = datetime.fromisoformat(last_accessed)
                else:
                    base_time = last_accessed.to_native()
            else:
                base_time = created_at_dt

            if base_time.tzinfo is None:
                base_time = base_time.replace(tzinfo=timezone.utc)

            decayed_strength = apply_time_decay(
                base_time,
                base_strength
            )

            # Cognitive state
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
    if not memory_ids:
        return

    now = datetime.now(timezone.utc)
    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE m.id IN $memory_ids
    SET m.strength =
        CASE
            WHEN m.archived = true THEN 0.6
            WHEN m.strength IS NULL THEN $boost
            WHEN m.strength + $boost > 1.0 THEN 1.0
            ELSE m.strength + $boost
        END,
        m.archived = false,
        m.last_accessed = $now
    """

    with driver.session() as session:
        session.run(
            query,
            memory_ids=memory_ids,
            boost=boost,
            now=now
        )


# ARCHIVE

def archive_faded_memories(threshold: float = 0.3):
    driver = get_driver()

    query = """
    MATCH (m:Memory)
    WHERE coalesce(m.strength, 0.8) <= $threshold
    SET m.archived = true
    """

    with driver.session() as session:
        session.run(query, threshold=threshold)