from fastapi import APIRouter, HTTPException, Query

from src.api.supabase import supabase

router = APIRouter(prefix="/api/v1", tags=["loans"])


@router.get("/loans")
def get_loans(status: str | None = Query(default="pending")):
    query = supabase.table("loans").select("*")
    if status:
        query = query.eq("status", status)

    response = query.execute()
    return response.data or []


@router.get("/loans/pending")
def get_pending_loans_alias():
    return get_loans(status="pending")


def _update_loan_status(loan_id: int, status: str):
    response = (
        supabase.table("loans")
        .update({"status": status})
        .eq("id", loan_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Loan not found")

    return response.data[0]


@router.post("/loans/{loan_id}/approve")
def approve_loan(loan_id: int):
    return _update_loan_status(loan_id, "approved")


@router.post("/loans/{loan_id}/deny")
def deny_loan(loan_id: int):
    return _update_loan_status(loan_id, "denied")
