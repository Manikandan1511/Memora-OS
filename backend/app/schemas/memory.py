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
