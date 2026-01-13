# backend/app/api/memory.py

from fastapi import APIRouter
from app.schemas.memory import (
    MemoryCreate,
    MemorySearchRequest,
    MemoryTimeRangeRequest
)
from app.services.ingestion import ingest_memory
from app.services.search import search_memories
from app.services.temporal import get_memories_by_time

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.post("/")
def add_memory(payload: MemoryCreate):
    return ingest_memory(
        content=payload.content,
        source=payload.source
    )


@router.post("/search")
def search(payload: MemorySearchRequest):
    return {
        "results": search_memories(
            query=payload.query,
            limit=payload.limit
        )
    }


@router.post("/timeline")
def timeline(payload: MemoryTimeRangeRequest):
    return {
        "results": get_memories_by_time(
            start_date=payload.start_date,
            end_date=payload.end_date
        )
    }
