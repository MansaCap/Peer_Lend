from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class BorrowerPaybackStatus:
	status_id: int
	loan_id: int
	borrower_id: int
	current_status: str
	last_payment_date: datetime | None
	next_due_date: datetime | None
	days_past_due: int = 0
	total_paid: float = 0.0
	outstanding_amount: float = 0.0
	risk_flag: str = "low"
	updated_at: datetime | None = None

	def to_dict(self) -> dict[str, Any]:
		return {
			"status_id": self.status_id,
			"loan_id": self.loan_id,
			"borrower_id": self.borrower_id,
			"current_status": self.current_status,
			"last_payment_date": self.last_payment_date,
			"next_due_date": self.next_due_date,
			"days_past_due": self.days_past_due,
			"total_paid": self.total_paid,
			"outstanding_amount": self.outstanding_amount,
			"risk_flag": self.risk_flag,
			"updated_at": self.updated_at,
		}
