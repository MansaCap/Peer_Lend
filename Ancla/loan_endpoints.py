from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
import os

app = FastAPI()

# --- Database connection ---
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "fintech")
    )

# --- Models ---
class Loan(BaseModel):
    borrower_id: int
    principal: float
    status: str
    collateral_value: float  # needed for LTV

# --- Risk Analysis Function ---
def analyze_loan(principal: float, collateral_value: float):
    # Placeholder logic — replace with MLflow model later
    credit_score = 680.0  # demo value
    pd = 0.12             # demo probability of default
    ltv = principal / collateral_value if collateral_value else None
    return credit_score, pd, ltv

# --- Endpoint ---
@app.post("/loans/create")
def create_loan(loan: Loan):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        credit_score, pd, ltv = analyze_loan(loan.principal, loan.collateral_value)

        cursor.execute(
            """
            INSERT INTO loans (borrower_id, principal, status, credit_score, pd, ltv)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (loan.borrower_id, loan.principal, loan.status, credit_score, pd, ltv)
        )
        conn.commit()
        return {
            "message": "Loan created successfully",
            "risk_metrics": {
                "credit_score": credit_score,
                "pd": pd,
                "ltv": ltv
            }
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
