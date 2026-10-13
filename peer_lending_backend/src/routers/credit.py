# Router for managing credit score-related operations, including scoring and retrieving credit scores for borrowers. #
# This router provides endpoints for scoring a borrower's credit and retrieving their credit score. #


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db

from services.credit_service import CreditService
from schemas.credit import CreditScoreRequest

router = APIRouter()
service = CreditService()

@router.post("/score")
def score(payload: CreditScoreRequest, db: Session = Depends(get_db)):
    return service.score(db, payload)

@router.get("/retrieve/{borrower_id}")
def retrieve_score(borrower_id: int, db: Session = Depends(get_db)):
    payload = CreditScoreRequest(borrower_id=borrower_id)
    return service.score(db, payload)
