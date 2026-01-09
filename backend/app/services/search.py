# backend/app/services/search.py

from app.services.embedding import generate_embedding
from app.db.chroma import collection

def search_memories(query: str, limit: int = 5):
    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )

    memories = []

    for i in range(len(results["ids"][0])):
        memories.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return memories
