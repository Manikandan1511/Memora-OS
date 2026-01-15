def generate_answer(question: str, memories: list) -> str:
    """
    Generate an answer using retrieved memories.
    Phase 1: deterministic reasoning (LLM-ready).
    """

    if not memories:
        return (
            "I could not find any relevant memories related to your question yet. "
            "Try adding more information to Memora OS."
        )

    context = "\n".join(
        [f"- {m['content']}" for m in memories]
    )

    prompt = f"""
You are Memora OS, a personal AI memory system.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Rules:
- Be concise
- Be accurate
- Do not hallucinate
"""

    # Phase 1: placeholder (safe & testable)
    answer = (
        "Based on your stored memories, here is what I found:\n\n"
        f"{context}"
    )

    return answer
