from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from src.api.payback import create_fastapi_app, handle_payback_request
from src.models.borrower import BorrowerPaybackStatus


class PaybackApiTests(unittest.TestCase):
	def setUp(self) -> None:
		self.status_store = {
			7: BorrowerPaybackStatus(
				status_id=77,
				loan_id=7,
				borrower_id=21,
				current_status="on_time",
				last_payment_date=None,
				next_due_date=None,
				days_past_due=0,
				total_paid=250.0,
				outstanding_amount=750.0,
				risk_flag="low",
				updated_at=None,
			)
		}
		self.client = TestClient(create_fastapi_app(self.status_store))

	def test_handle_payback_request_returns_live_status(self) -> None:
		status_code, payload = handle_payback_request(
			"GET",
			"/borrower/payback/status/7",
			self.status_store,
		)

		self.assertEqual(200, status_code.value)
		self.assertEqual(7, payload["loan_id"])
		self.assertEqual(21, payload["borrower_id"])
		self.assertEqual("healthy", payload["repayment_health"])
		self.assertEqual("borrower_payback_status", payload["status_source"])

	def test_handle_payback_request_returns_404_for_missing_loan(self) -> None:
		status_code, payload = handle_payback_request("GET", "/borrower/payback/status/404", self.status_store)

		self.assertEqual(404, status_code.value)
		self.assertEqual("borrower payback status not found", payload["error"])

	def test_fastapi_status_route_returns_json_response(self) -> None:
		response = self.client.get("/borrower/payback/status/7")

		self.assertEqual(200, response.status_code)
		payload = response.json()
		self.assertEqual(7, payload["loan_id"])
		self.assertEqual("healthy", payload["repayment_health"])

	def test_fastapi_payback_analyze_returns_tally(self) -> None:
		response = self.client.post("/payback/analyze", json={"loan_ids": [7, 404]})

		self.assertEqual(200, response.status_code)
		payload = response.json()
		self.assertEqual(2, payload["total_loans"])
		self.assertEqual(1, payload["tally"]["healthy"])
		self.assertEqual(1, payload["tally"]["not_found"])


if __name__ == "__main__":
	unittest.main()
