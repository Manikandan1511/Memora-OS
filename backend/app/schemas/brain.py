from pydantic import BaseModel, Field
from typing import List


class BrainAskRequest(BaseModel):
    question: str = Field(
        ..., 
        min_length=3, 
        description="User question to ask Memora OS"
    )


class MemoryHit(BaseModel):
    id: str
    content: str
    score: float


class BrainAskResponse(BaseModel):
    answer: str
    memories_used: List[MemoryHit]