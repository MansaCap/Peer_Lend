#Credit score placeholder.#
#Matches your PD/LTV scoring entities$

from fastapi import APIRouter

router = APIRouter()

@router.post("/score")
def score(payload: dict):
    return {"message": "Credit score placeholder", "payload": payload}

@router.get("/retrieve/{borrower_id}")
def retrieve_score(borrower_id: int):
    return {"borrower_id": borrower_id, "score": "placeholder"}
