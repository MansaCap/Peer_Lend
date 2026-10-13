# Service class for calculating credit scores based on a borrower's loan and repayment history. #


from sqlalchemy.orm import Session
from repositories.loan_repository import LoanRepository
from repositories.repayment_repository import RepaymentRepository
from schemas.credit import CreditScoreRequest, CreditScoreResponse

class CreditService:
    def __init__(self):
        self.loans = LoanRepository()
        self.repayments = RepaymentRepository()

    def score(self, db: Session, payload: CreditScoreRequest) -> CreditScoreResponse:
        loans = self.loans.list_by_borrower(db, payload.borrower_id)
        if not loans:
            return CreditScoreResponse(borrower_id=payload.borrower_id, score=0.0)

        # Simple placeholder scoring logic
        total_amount = sum([float(l.amount) for l in loans])
        score = max(300.0, 850.0 - total_amount / 1000.0)

        return CreditScoreResponse(borrower_id=payload.borrower_id, score=score)
