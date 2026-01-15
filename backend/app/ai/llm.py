# backend/app/ai/llm.py

from collections import OrderedDict


def _deduplicate_contents(items: list[str]) -> list[str]:
    """
    Preserve order while removing duplicates.
    """
    return list(OrderedDict.fromkeys(items))


def _summarize_points(points: list[str]) -> str:
    """
    Convert bullet-like facts into a natural sentence.
    """
    if not points:
        return ""

    if len(points) == 1:
        return points[0]

    if len(points) == 2:
        return f"{points[0]} and {points[1]}"

    return ", ".join(points[:-1]) + f", and {points[-1]}"


def generate_answer(
    question: str,
    memories: list,
    graph_context: list | None = None
) -> str:

    if not memories:
        return (
            "I don’t have enough stored information yet to answer this question. "
            "Try adding more memories to Memora OS."
        )

    # Extract & clean memory facts
    memory_points = [
        m["content"].strip().rstrip(".")
        for m in memories
        if m.get("content")
    ]

    memory_points = _deduplicate_contents(memory_points)

    # Extract graph-related facts
    graph_points = []
    if graph_context:
        for g in graph_context:
            content = g.get("content")
            relation = g.get("relation")
            if content and relation:
                graph_points.append(
                    f"{content.strip()} (linked via {relation.lower()})"
                )

    graph_points = _deduplicate_contents(graph_points)

    # Summarize
    memory_summary = _summarize_points(memory_points)

    answer_parts = []

    answer_parts.append(
        "Based on your stored memories and their relationships, here is my assessment:"
    )

    if memory_summary:
        answer_parts.append(
            f"Overall, {memory_summary}."
        )

    if graph_points:
        graph_summary = _summarize_points(graph_points)
        answer_parts.append(
            f"Related concepts in your knowledge graph further support this, including {graph_summary}."
        )

    # Final answer
    return "\n\n".join(answer_parts)
