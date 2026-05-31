from __future__ import annotations


def derive_repayment_health(current_status: str, days_past_due: int, risk_flag: str, outstanding_amount: float) -> str:
	if current_status == "completed" or outstanding_amount <= 0:
		return "completed"

	if current_status == "defaulted" or risk_flag == "high" or days_past_due >= 30:
		return "critical"

	if current_status == "late" or risk_flag == "medium" or days_past_due > 0:
		return "watch"

	return "healthy"
