from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MemoryCreate(BaseModel):
    content: str
    source: Optional[str] = "manual"

class MemoryResponse(BaseModel):
    id: str
    content: str
    source: str
    embedding: List[float]
    created_at: datetime


class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 5

class MemorySearchResult(BaseModel):
    id: str
    content: str
    metadata: dict

class MemorySearchResponse(BaseModel):
    results: List[MemorySearchResult]

class MemoryTimeRangeRequest(BaseModel):
    start_date: str  # ISO format
    end_date: str    # ISO format

class MemoryTimeRangeResponse(BaseModel):
    results: List[MemorySearchResult]
