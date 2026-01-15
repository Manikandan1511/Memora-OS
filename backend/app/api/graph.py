# backend/app/api/graph.py

from fastapi import APIRouter
from app.services.graph import (
    get_graph,
    get_memory_timeline
)

router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)


@router.get("/")
def read_graph():
    return get_graph()


@router.get("/timeline")
def read_timeline():
    return {
        "timeline": get_memory_timeline(limit=50)
    }
