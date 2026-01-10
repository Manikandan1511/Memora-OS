# backend/app/services/temporal.py

from datetime import datetime
from app.db.chroma import collection

def get_memories_by_time(start_date: str, end_date: str):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    results = collection.get(
        include=["documents", "metadatas"]
    )

    memories = []

    for i, meta in enumerate(results["metadatas"]):
        created_at = datetime.fromisoformat(meta["created_at"])
        if start <= created_at <= end:
            memories.append({
                "id": results["ids"][i],        # ids are always returned
                "content": results["documents"][i],
                "metadata": meta
            })

    return memories
