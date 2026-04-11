from app.db.chroma import semantic_search
from app.services.graph import (
    expand_context_from_memories,
    get_memory_timeline,
    reinforce_memories
)
from app.ai.llm import generate_answer


def ask_brain(question: str):
    """
    Core reasoning pipeline of Memora OS.

    Flow:
    1. Semantic recall (vector DB)
    2. Reinforce + revive recalled memories
    3. Graph-based context expansion
    4. Timeline-based reasoning
    5. LLM answer generation
    """

    # STEP 1: Vector recall
    memories = semantic_search(
        query=question,
        k=5
    )

    # Extract memory IDs
    memory_ids = [m["id"] for m in memories]

    # 🔥 STEP 2: Reinforce + REVIVE memories
    if memory_ids:
        reinforce_memories(memory_ids)

    # 🚨 DO NOT ARCHIVE HERE (handled by decay engine)

    # STEP 3: Graph reasoning
    graph_context = expand_context_from_memories(
        memory_ids=memory_ids,
        limit=5
    )

    # STEP 4: Timeline reasoning
    timeline = get_memory_timeline(limit=10)

    # STEP 5: Generate final answer
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