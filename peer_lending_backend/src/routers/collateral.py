# Router for managing collateral-related operations, including adding, listing, and verifying collateral. #
# This router provides endpoints for adding new collateral, listing collateral for a specific borrower, and verifying collateral. #

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db

from services.collateral_service import CollateralService
from schemas.collateral import CollateralCreate

router = APIRouter()
service = CollateralService()

@router.post("/add")
def add_collateral(payload: CollateralCreate, db: Session = Depends(get_db)):
    return service.add_collateral(db, payload)

@router.get("/borrower/{borrower_id}")
def list_collateral(borrower_id: int, db: Session = Depends(get_db)):
    return service.list_for_borrower(db, borrower_id)

@router.post("/verify/{collateral_id}")
def verify_collateral(collateral_id: int, db: Session = Depends(get_db)):
    return service.verify(db, collateral_id)
