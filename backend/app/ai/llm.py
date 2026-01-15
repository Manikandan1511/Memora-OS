from collections import OrderedDict


def _dedupe(items):
    return list(OrderedDict.fromkeys(items))


def generate_answer(
    question: str,
    memories: list,
    graph_context: list | None = None,
    timeline: list | None = None
) -> str:

    if not memories:
        return (
            "I don’t have enough stored information yet to answer this question. "
            "Try adding more memories to Memora OS."
        )

    # Memory facts

    memory_points = _dedupe(
        m["content"].strip().rstrip(".")
        for m in memories
        if m.get("content")
    )

    # Graph facts
    graph_points = []
    if graph_context:
        for g in graph_context:
            if g.get("content"):
                graph_points.append(
                    f"{g['content']} (linked via {g['relation'].lower()})"
                )
    graph_points = _dedupe(graph_points)

    # Timeline analysis
    timeline_summary = ""
    if timeline and len(timeline) >= 2:
        early = timeline[0]["content"].strip()
        recent = timeline[-1]["content"].strip()

        if early != recent:
            timeline_summary = (
                f"Initially, {early}. "
                f"Over time, this progressed, and more recently, {recent}."
            )

    # Compose answer
    answer_parts = []

    answer_parts.append(
        "Based on your memories, their relationships, and how they evolved over time, here is my assessment:"
    )

    if memory_points:
        answer_parts.append(
            "Overall, " + ", ".join(memory_points[:-1]) +
            f", and {memory_points[-1]}."
            if len(memory_points) > 1
            else f"Overall, {memory_points[0]}."
        )

    if graph_points:
        answer_parts.append(
            "Related concepts in your knowledge graph further support this, including "
            + ", ".join(graph_points) + "."
        )

    if timeline_summary:
        answer_parts.append(timeline_summary)

    return "\n\n".join(answer_parts)
