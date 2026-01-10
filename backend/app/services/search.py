# backend/app/services/search.py

from app.db.chroma import get_collection
from app.services.embedding import create_embedding

collection = get_collection()


def search_memories(query: str, limit: int = 5):
    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        include=["documents", "metadatas"]  # ❗ NO "ids"
    )

    memories = []

    for i in range(len(results["documents"][0])):
        memories.append({
            "id": results["ids"][0][i],  # ✅ ids still available here
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return memories
