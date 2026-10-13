# Router for demo credit scoring and retrieving recently computed scores.

from fastapi import APIRouter, HTTPException, status

from peer_lending_backend.src.schemas.credit import CreditScoreRequest
from peer_lending_backend.src.services.credit_service import CreditService

router = APIRouter()
service = CreditService()


@router.post("/score")
def score(payload: CreditScoreRequest):
    return service.score(payload)


@router.get("/retrieve/{borrower_id}")
def retrieve_score(borrower_id: int):
    result = service.retrieve(borrower_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No score has been calculated for this borrower in this process",
        )
    return result