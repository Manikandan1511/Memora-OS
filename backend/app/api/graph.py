# backend/app/api/graph.py

from fastapi import APIRouter
from app.services.graph import get_graph

router = APIRouter(prefix="/graph", tags=["Graph"])


@router.get("/")
def read_graph():
    return get_graph()
