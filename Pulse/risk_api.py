from fastapi import FastAPI, HTTPException
import pandas as pd
import mlflow
import mysql.connector
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Pulse Lending Risk Engine API")

lgb_model: Optional[object] = None
xgb_model: Optional[object] = None


# Database connection (adjust with your credentials)
def get_db_connection():
    return mysql.connector.connect(
         host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "fintech"
    )


# --- Models ---
class Loan(BaseModel):
    borrower_id: int
    principal: float
    status: str


class Repayment(BaseModel):
    loan_id: int
    amount: float


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
                "INSERT INTO loans (borrower_id, principal, status) "
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
            "INSERT INTO repayments (loan_id, amount) VALUES (%s, %s)",
            (repayment.loan_id, repayment.amount)
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
