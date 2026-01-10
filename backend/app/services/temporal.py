# backend/app/services/temporal.py

from datetime import datetime
from app.db.chroma import get_collection


def get_memories_by_time(start_date: str, end_date: str):
    collection = get_collection()

    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    results = collection.get(
        include=["documents", "metadatas"]
    )

    memories = []

    for i in range(len(results["documents"])):
        metadata = results["metadatas"][i]
        created_at = datetime.fromisoformat(metadata["created_at"])

        if start <= created_at <= end:
            memories.append({
                "id": results["ids"][i],
                "content": results["documents"][i],
                "metadata": metadata
            })

    return memories
