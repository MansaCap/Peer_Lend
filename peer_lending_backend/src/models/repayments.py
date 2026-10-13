# SQL Alchemy model for the Repayment table #

from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from peer_lending_backend.src.db.database import Base

class Repayment(Base):
    __tablename__ = "repayments"

    repayment_id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.loan_id"))
    amount = Column(DECIMAL(10, 2))
    paid_at = Column(DateTime)

    loan = relationship("Loan")
