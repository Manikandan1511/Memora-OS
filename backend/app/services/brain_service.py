# backend/app/services/brain_service.py

from app.db.chroma import semantic_search
from app.services.graph import expand_context_from_memories
from app.ai.llm import generate_answer


def ask_brain(question: str):
    """
    AskBrain with Vector + Neo4j Graph reasoning.
    """

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

    # Step 3: Answer generation
    answer = generate_answer(
        question=question,
        memories=memories,
        graph_context=graph_context
    )

    return {
        "answer": answer,
        "memories_used": memories,
        "graph_context": graph_context
    }
