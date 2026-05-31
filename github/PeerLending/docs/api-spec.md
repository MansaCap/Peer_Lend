# API Spec

## GET /borrower/payback/status/{loan_id}

Returns the current repayment snapshot for a loan from `borrower_payback_status`.

Response fields include the source row plus a derived `repayment_health` value for dashboards and risk models.

Example payload:

```json
{
  "status_id": 1,
  "loan_id": 1001,
  "borrower_id": 501,
  "current_status": "on_time",
  "last_payment_date": "2026-05-27T14:30:00Z",
  "next_due_date": "2026-06-10T14:30:00Z",
  "days_past_due": 0,
  "total_paid": 1250.0,
  "outstanding_amount": 3750.0,
  "risk_flag": "low",
  "updated_at": "2026-05-29T09:00:00Z",
  "repayment_health": "healthy",
  "status_source": "borrower_payback_status"
}
```

## POST /payback/analyze

Aggregates repayment health for a batch of loans and returns a tally summary.

Request body:

```json
{
  "loan_ids": [1001, 1002, 9999]
}
```

Response body:

```json
{
  "analyzed_at": "2026-05-29T10:30:00Z",
  "total_loans": 3,
  "tally": {
    "healthy": 1,
    "watch": 1,
    "critical": 0,
    "completed": 0,
    "not_found": 1
  },
  "results": [
    {"loan_id": 1001, "repayment_health": "healthy", "status": "found"},
    {"loan_id": 1002, "repayment_health": "watch", "status": "found"},
    {"loan_id": 9999, "repayment_health": null, "status": "not_found"}
  ]
}
```

The route output can be written into `payback_analysis_tally` for reporting and dashboard trend views.
