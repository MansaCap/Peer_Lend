# API Spec

## GET /borrower/payback/status/{loan_id}

Returns the current repayment snapshot for a loan from `borrower_payback_status`.

Response fields include the source row plus a derived `repayment_health` value for dashboards and risk models.

## POST /payback/analyze

Writes an aggregate snapshot for portfolio-level credit indicators.

The endpoint computes averages from `borrower_payback_status` and inserts one row into `payback_analysis_tally`.

The route can be called at both `/payback/analyze` and `/borrower/payback/analyze`.
