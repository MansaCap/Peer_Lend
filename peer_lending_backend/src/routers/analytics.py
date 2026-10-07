from collections import Counter

from fastapi import APIRouter

from peer_lending_backend.src.supabase_client import supabase

router = APIRouter(prefix="/api", tags=["analytics"])


@router.get("/analytics")
def get_analytics():
    repayments_response = (
        supabase.table("repayments")
        .select("due_date,amount_due,status")
        .order("due_date")
        .execute()
    )
    repayments = repayments_response.data or []

    loans_response = supabase.table("loans").select("status").execute()
    statuses = [
        row.get("status") or "unknown"
        for row in (loans_response.data or [])
    ]
    status_counts = Counter(statuses)

    loan_status = [
        {"status": status, "count": count}
        for status, count in sorted(
            status_counts.items(),
            key=lambda item: item[0],
        )
    ]

    return {"repayments": repayments, "loan_status": loan_status}
