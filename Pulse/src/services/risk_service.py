# Service class for computing borrower risk status and portfolio analysis tally. #


from sqlalchemy.orm import Session
from models.borrower_payback_status import BorrowerPaybackStatus
from models.payback_analysis_tally import PaybackAnalysisTally

class RiskService:
    def compute_borrower_status(self, db: Session, borrower_id: int):
        # Placeholder: fetch and return existing status
        return db.query(BorrowerPaybackStatus).filter(
            BorrowerPaybackStatus.borrower_id == borrower_id
        ).first()

    def compute_portfolio_tally(self, db: Session):
        return db.query(PaybackAnalysisTally).first()
