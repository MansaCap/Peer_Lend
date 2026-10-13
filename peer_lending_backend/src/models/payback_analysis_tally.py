# SQL Alchemy model for the Payback Analysis Tally table #
from sqlalchemy import Column, Integer, DECIMAL
try:
    from db.database import Base
except ModuleNotFoundError:
    from peer_lending_backend.src.db.database import Base


class PaybackAnalysisTally(Base):
    __tablename__ = "payback_analysis_tally"

    tally_id = Column(Integer, primary_key=True, index=True)
    total_loans = Column(Integer)
    avg_pd = Column(DECIMAL(5, 2))   # Probability of Default
    avg_ltv = Column(DECIMAL(5, 2))  # Loan-to-Value
    avg_repayment_time = Column(Integer)
