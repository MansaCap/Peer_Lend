from fastapi import FastAPI, Query
from ..endpoints import loan_endpoints

app = FastAPI()
app.include_router(loan_endpoints.router)

# Existing implementation (query param style)
@app.get("/api/v1/repayments")
def get_repayments(loan_id: int = Query(...)):
    # your existing logic here
    return {"loan_id": loan_id, "repayments": []}

@app.get("/api/v1/loans")
def get_loans(status: str = Query(...)):
    # your existing logic here
    return {"status": status, "loans": []}

# 🔹 Backward-compatible aliases

@app.get("/api/v1/repayments/{loan_id}")
def get_repayments_alias(loan_id: int):
    # simply call the same logic as the query-param version
    return get_repayments(loan_id=loan_id)

@app.get("/api/v1/loans/pending")
def get_pending_loans_alias():
    # call the same logic as the query-param version
    return get_loans(status="pending")
