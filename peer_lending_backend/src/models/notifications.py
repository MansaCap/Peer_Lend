# SQL Alchemy model for the Notifications table #
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.database import Base


class NotificationChannel(str, enum.Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    IN_APP = "IN_APP"


class NotificationPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    channel = Column(Enum(NotificationChannel), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    priority = Column(Enum(NotificationPriority), default=NotificationPriority.LOW, index=True)
    related_loan_id = Column(Integer, ForeignKey("loans.loan_id", ondelete="SET NULL"), nullable=True)
    related_txn_id = Column(Integer, ForeignKey("transactions.transaction_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    read_at = Column(DateTime, nullable=True)

    user = relationship("User")
    loan = relationship("Loan")
    transaction = relationship("Transaction")
