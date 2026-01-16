from app.db.chroma import semantic_search
from app.services.graph import (
    expand_context_from_memories,
    get_memory_timeline
)
from app.ai.llm import generate_answer


def ask_brain(question: str):

    # Step 1: Vector recall
    memories = semantic_search(
        query=question,
        k=5
    )

    memory_ids = [m["id"] for m in memories]

    # Step 2: Graph reasoning
    graph_context = expand_context_from_memories(
        memory_ids=memory_ids,
        limit=5
    )

    # Step 3: Timeline reasoning
    timeline = get_memory_timeline(limit=10)

    # Step 4: Final answer
    answer = generate_answer(
        question=question,
        memories=memories,
        graph_context=graph_context,
        timeline=timeline
    )

    return {
        "answer": answer,
        "memories_used": memories,
        "graph_context": graph_context,
        "timeline_used": timeline
    }