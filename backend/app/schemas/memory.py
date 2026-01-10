# backend/app/schemas/memory.py

from pydantic import BaseModel


# -------- Request Schemas --------

class MemoryCreateRequest(BaseModel):
    content: str
    source: str


class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 5


class MemoryTimelineRequest(BaseModel):
    start_date: str
    end_date: str


# -------- Response Schemas --------

class MemoryResponse(BaseModel):
    id: str
    content: str
    source: str
    created_at: str
