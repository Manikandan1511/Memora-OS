from fastapi import APIRouter, HTTPException
from app.schemas.brain import (
    BrainAskRequest,
    BrainAskResponse
)
from app.services.brain_service import ask_brain

router = APIRouter(
    prefix="/brain",
    tags=["Brain"]
)


@router.post(
    "/ask",
    response_model=BrainAskResponse
)
def ask(payload: BrainAskRequest):
    try:
        return ask_brain(payload.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
