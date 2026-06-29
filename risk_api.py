import os
from collections import defaultdict, deque
from threading import Lock
from time import time
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd
import mlflow
import mysql.connector
from pydantic import BaseModel

app = FastAPI(title="Pulse Lending Risk Engine API")

lgb_model: Optional[object] = None
xgb_model: Optional[object] = None

RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
_request_buckets: dict[str, deque[float]] = defaultdict(deque)
_rate_limit_lock = Lock()


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Keep docs and schema available for tooling and health checks.
    if request.url.path in {"/docs", "/openapi.json", "/redoc"}:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    with _rate_limit_lock:
        bucket = _request_buckets[client_ip]
        while bucket and bucket[0] < window_start:
            bucket.popleft()

        if len(bucket) >= RATE_LIMIT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": (
                        f"Rate limit exceeded: {RATE_LIMIT_REQUESTS} requests "
                        f"per {RATE_LIMIT_WINDOW_SECONDS} seconds."
                    )
                },
            )

        bucket.append(now)

    return await call_next(request)


# Database connection (adjust with your credentials)
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "fintech"),
    )


# --- Models ---
class Loan(BaseModel):
    borrower_id: int
    principal: float
    status: str


class Repayment(BaseModel):
    loan_id: int
    amount: float
    source: str = "bank_transfer"


class ComplianceLog(BaseModel):
    user_id: int
    action: str


# --- Endpoints ---
@app.post("/loans/create")
def create_loan(loan: Loan):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            (
                "INSERT INTO loans (borrower_id, principal_amount, status) "
                "VALUES (%s, %s, %s)"
            ),
            (loan.borrower_id, loan.principal, loan.status),
        )
        conn.commit()
        return {"message": "Loan created successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    finally:
        cursor.close()
        conn.close()


@app.post("/repayments/add")
def add_repayment(repayment: Repayment):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT borrower_id FROM loans WHERE loan_id = %s",
            (repayment.loan_id,),
        )
        loan_row = cursor.fetchone()
        if loan_row is None:
            raise HTTPException(status_code=404, detail="Loan not found")
        borrower_id = int(loan_row[0])

        cursor.execute(
            (
                "INSERT INTO repayments "
                "(loan_id, borrower_id, amount, source, payment_date) "
                "VALUES (%s, %s, %s, %s, NOW())"
            ),
            (
                repayment.loan_id,
                borrower_id,
                repayment.amount,
                repayment.source,
            ),
        )
        conn.commit()
        return {"message": "Repayment added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    finally:
        cursor.close()
        conn.close()


@app.post("/compliance/log")
def log_compliance(entry: ComplianceLog):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO compliance_logs (user_id, action) VALUES (%s, %s)",
            (entry.user_id, entry.action)
        )
        conn.commit()
        return {"message": "Compliance log entry created"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    finally:
        cursor.close()
        conn.close()


# Load registered models from MLflow
def load_models() -> tuple[Optional[object], Optional[object]]:
    try:
        lgb = mlflow.sklearn.load_model(
            "models:/Pulse_Lending_LightGBM/Production"
        )
    except Exception:
        lgb = None

    try:
        xgb = mlflow.sklearn.load_model(
            "models:/Pulse_Lending_XGBoost/Production"
        )
    except Exception:
        xgb = None

    return lgb, xgb


lgb_model, xgb_model = load_models()


@app.post("/score")
def score_endpoint(
    age: float, income: float, group_size: int, alpha: float = 0.5
):
    if lgb_model is None or xgb_model is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Scoring models are unavailable. Register "
                "Pulse_Lending_LightGBM and Pulse_Lending_XGBoost in MLflow."
            ),
        )

    x_row = pd.DataFrame(
        [[age, income, group_size]], columns=["age", "income", "group_size"]
    )
    lgb_p = lgb_model.predict(x_row)[0]
    xgb_p = xgb_model.predict(x_row)[0]
    final_p = alpha * lgb_p + (1 - alpha) * xgb_p
    return {"risk_score": final_p}
