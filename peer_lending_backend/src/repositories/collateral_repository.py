# Repository class for managing Collateral entities in the database using SQLAlchemy #

from sqlalchemy.orm import Session
from models.collateral import Collateral
from schemas.collateral import CollateralCreate

class CollateralRepository:
    def create(self, db: Session, payload: CollateralCreate):
        collateral = Collateral(
            borrower_id=payload.borrower_id,
            type=payload.type,
            value=payload.value,
            verification_status=payload.verification_status,
        )
        db.add(collateral)
        db.commit()
        db.refresh(collateral)
        return collateral

    def list_by_borrower(self, db: Session, borrower_id: int):
        return db.query(Collateral).filter(Collateral.borrower_id == borrower_id).all()

    def update_status(self, db: Session, collateral_id: int, status: str):
        collateral = db.query(Collateral).filter(
            Collateral.collateral_id == collateral_id
        ).first()
        if not collateral:
            return None
        collateral.verification_status = status
        db.commit()
        db.refresh(collateral)
        return collateral
