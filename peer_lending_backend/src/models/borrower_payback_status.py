# SQL Alchemy model for the Borrower Payback Status table #
from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class BorrowerPaybackStatus(Base):
    __tablename__ = "borrower_payback_status"

    status_id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("users.user_id"))
    total_loans = Column(Integer)
    total_repaid = Column(DECIMAL(10, 2))
    delinquency_rate = Column(DECIMAL(5, 2))
    risk_grade = Column(String(10))

    borrower = relationship("User")
