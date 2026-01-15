from app.db.chroma import semantic_search
from app.ai.llm import generate_answer


def ask_brain(question: str):
    """
    Core orchestration logic for AskBrain.
    """

    # Step 1: semantic recall
    memories = semantic_search(
        query=question,
        k=5
    )

    # Step 2: reasoning
    answer = generate_answer(
        question=question,
        memories=memories
    )

    # Step 3: response
    return {
        "answer": answer,
        "memories_used": memories
    }
