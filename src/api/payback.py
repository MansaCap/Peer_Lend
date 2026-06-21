from datetime import date, timedelta
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.api.supabase import supabase

router = APIRouter(prefix="/api/v1", tags=["repayments"])


class RepaymentScheduleItem(BaseModel):
    due_date: date
    amount_due: float
    status: str  # "Pending", "Paid", "Late"


class PaybackRequest(BaseModel):
    loan_id: int
    principal: float
    term: int  # months
    interest_rate: float  # annual %


class PaybackResponse(BaseModel):
    loan_id: int
    schedule: List[RepaymentScheduleItem]
    next_payment: Optional[RepaymentScheduleItem]


@router.post("/schedule", response_model=PaybackResponse)
def generate_schedule(request: PaybackRequest):
    if request.term <= 0:
        raise HTTPException(status_code=400, detail="Term must be positive")

    monthly_rate = request.interest_rate / 12 / 100
    monthly_payment = (request.principal * monthly_rate) / (
        1 - (1 + monthly_rate) ** -request.term
    )

    schedule = []
    start_date = date.today()

    for i in range(request.term):
        due = start_date + timedelta(days=30 * (i + 1))
        schedule.append(RepaymentScheduleItem(
            due_date=due,
            amount_due=round(monthly_payment, 2),
            status="Pending",
        ))

    next_payment = schedule[0] if schedule else None
    return PaybackResponse(
        loan_id=request.loan_id,
        schedule=schedule,
        next_payment=next_payment,
    )


@router.get("/repayments")
def get_repayments(loan_id: int | None = Query(default=None)):
    query = supabase.table("repayments").select("*")
    if loan_id is not None:
        query = query.eq("loan_id", loan_id)

    response = query.execute()
    return response.data or []


@router.get("/repayments/{loan_id}")
def get_repayments_alias(loan_id: int):
    return get_repayments(loan_id=loan_id)


@router.post("/payback/schedule", response_model=PaybackResponse)
def legacy_generate_schedule(request: PaybackRequest):
    return generate_schedule(request)


