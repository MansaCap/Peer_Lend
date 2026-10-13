# Service class for managing collateral, including adding, listing, and verifying collateral. #

from sqlalchemy.orm import Session
from repositories.collateral_repository import CollateralRepository
from schemas.collateral import CollateralCreate

class CollateralService:
    def __init__(self):
        self.repo = CollateralRepository()

    def add_collateral(self, db: Session, payload: CollateralCreate):
        return self.repo.create(db, payload)

    def list_for_borrower(self, db: Session, borrower_id: int):
        return self.repo.list_by_borrower(db, borrower_id)

    def verify(self, db: Session, collateral_id: int, status: str = "verified"):
        return self.repo.update_status(db, collateral_id, status)
