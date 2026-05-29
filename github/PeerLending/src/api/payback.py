from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Any
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.models.borrower import BorrowerPaybackStatus
from src.services.scoring import derive_repayment_health

PAYBACK_STATUS_ROUTE_PREFIX = "/borrower/payback/status/"

PaybackStatusStore = Mapping[int, BorrowerPaybackStatus] | Callable[[int], BorrowerPaybackStatus | None]


class PaybackAnalyzeRequest(BaseModel):
	loan_ids: list[int] = Field(min_length=1)


class PaybackAnalyzeResult(BaseModel):
	loan_id: int
	repayment_health: str | None
	status: str


class PaybackAnalyzeTally(BaseModel):
	healthy: int
	watch: int
	critical: int
	completed: int
	not_found: int


class PaybackAnalyzeResponse(BaseModel):
	analyzed_at: str
	total_loans: int
	tally: PaybackAnalyzeTally
	results: list[PaybackAnalyzeResult]


DEFAULT_PAYBACK_STATUS_STORE: dict[int, BorrowerPaybackStatus] = {
	1001: BorrowerPaybackStatus(
		status_id=1,
		loan_id=1001,
		borrower_id=501,
		current_status="on_time",
		last_payment_date=datetime(2026, 5, 27, 14, 30, tzinfo=timezone.utc),
		next_due_date=datetime(2026, 6, 10, 14, 30, tzinfo=timezone.utc),
		days_past_due=0,
		total_paid=1250.0,
		outstanding_amount=3750.0,
		risk_flag="low",
		updated_at=datetime(2026, 5, 29, 9, 0, tzinfo=timezone.utc),
	),
	1002: BorrowerPaybackStatus(
		status_id=2,
		loan_id=1002,
		borrower_id=502,
		current_status="late",
		last_payment_date=datetime(2026, 5, 20, 11, 15, tzinfo=timezone.utc),
		next_due_date=datetime(2026, 5, 24, 11, 15, tzinfo=timezone.utc),
		days_past_due=5,
		total_paid=900.0,
		outstanding_amount=2100.0,
		risk_flag="medium",
		updated_at=datetime(2026, 5, 29, 9, 0, tzinfo=timezone.utc),
	),
}


def _serialize_datetime(value: datetime | None) -> str | None:
	if value is None:
		return None
	return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _serialize_status(status: BorrowerPaybackStatus) -> dict[str, Any]:
	payload = status.to_dict()
	payload["last_payment_date"] = _serialize_datetime(status.last_payment_date)
	payload["next_due_date"] = _serialize_datetime(status.next_due_date)
	payload["updated_at"] = _serialize_datetime(status.updated_at)
	payload["repayment_health"] = derive_repayment_health(
		status.current_status,
		status.days_past_due,
		status.risk_flag,
		status.outstanding_amount,
	)
	payload["status_source"] = "borrower_payback_status"
	return payload


def resolve_payback_status(loan_id: int, status_store: PaybackStatusStore | None = None) -> BorrowerPaybackStatus | None:
	store = DEFAULT_PAYBACK_STATUS_STORE if status_store is None else status_store

	if callable(store):
		return store(loan_id)

	return store.get(loan_id)


def get_borrower_payback_status(loan_id: int, status_store: PaybackStatusStore | None = None) -> dict[str, Any]:
	status = resolve_payback_status(loan_id, status_store)
	if status is None:
		raise KeyError(loan_id)

	return _serialize_status(status)


def analyze_payback_health(loan_ids: list[int], status_store: PaybackStatusStore | None = None) -> dict[str, Any]:
	tally = {
		"healthy": 0,
		"watch": 0,
		"critical": 0,
		"completed": 0,
		"not_found": 0,
	}
	results: list[dict[str, Any]] = []

	for loan_id in loan_ids:
		status = resolve_payback_status(loan_id, status_store)
		if status is None:
			tally["not_found"] += 1
			results.append(
				{
					"loan_id": loan_id,
					"repayment_health": None,
					"status": "not_found",
				}
			)
			continue

		repayment_health = derive_repayment_health(
			status.current_status,
			status.days_past_due,
			status.risk_flag,
			status.outstanding_amount,
		)
		tally[repayment_health] += 1
		results.append(
			{
				"loan_id": loan_id,
				"repayment_health": repayment_health,
				"status": "found",
			}
		)

	return {
		"analyzed_at": _serialize_datetime(datetime.now(timezone.utc)),
		"total_loans": len(loan_ids),
		"tally": tally,
		"results": results,
	}


def handle_payback_request(method: str, path: str, status_store: PaybackStatusStore | None = None) -> tuple[HTTPStatus, dict[str, Any]]:
	normalized_path = urlsplit(path).path
	if method.upper() != "GET" or not normalized_path.startswith(PAYBACK_STATUS_ROUTE_PREFIX):
		return HTTPStatus.NOT_FOUND, {"error": "route_not_found"}

	loan_id_text = normalized_path[len(PAYBACK_STATUS_ROUTE_PREFIX) :].strip("/")
	if not loan_id_text:
		return HTTPStatus.BAD_REQUEST, {"error": "loan_id is required"}

	try:
		loan_id = int(loan_id_text)
	except ValueError:
		return HTTPStatus.BAD_REQUEST, {"error": "loan_id must be an integer"}

	status = resolve_payback_status(loan_id, status_store)
	if status is None:
		return HTTPStatus.NOT_FOUND, {
			"error": "borrower payback status not found",
			"loan_id": loan_id,
		}

	return HTTPStatus.OK, _serialize_status(status)


def create_wsgi_app(status_store: PaybackStatusStore | None = None):
	def app(environ: dict[str, Any], start_response):
		status_code, payload = handle_payback_request(
			environ.get("REQUEST_METHOD", "GET"),
			environ.get("PATH_INFO", "/"),
			status_store,
		)
		body = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
		start_response(
			f"{status_code.value} {status_code.phrase}",
			[
				("Content-Type", "application/json; charset=utf-8"),
				("Content-Length", str(len(body))),
			],
		)
		return [body]

	return app


def create_fastapi_app(status_store: PaybackStatusStore | None = None) -> FastAPI:
	fastapi_app = FastAPI(title="PeerLending Payback API", version="1.0.0")
	fastapi_app.state.status_store = DEFAULT_PAYBACK_STATUS_STORE if status_store is None else status_store

	@fastapi_app.get("/borrower/payback/status/{loan_id}")
	def borrower_payback_status(loan_id: int) -> dict[str, Any]:
		status = resolve_payback_status(loan_id, fastapi_app.state.status_store)
		if status is None:
			raise HTTPException(status_code=404, detail=f"Borrower payback status not found for loan_id={loan_id}")

		return _serialize_status(status)

	@fastapi_app.post("/payback/analyze", response_model=PaybackAnalyzeResponse)
	def payback_analyze(request: PaybackAnalyzeRequest) -> dict[str, Any]:
		return analyze_payback_health(request.loan_ids, fastapi_app.state.status_store)

	return fastapi_app


app = create_fastapi_app()
