from fastapi import APIRouter

from src.api.supabase import supabase

router = APIRouter(prefix="/api/v1", tags=["notifications"])


@router.get("/notifications")
def get_notifications():
    response = supabase.table("notifications").select("*").execute()
    notifications = response.data or []

    return [
        {
            "id": note.get("id"),
            "type": note.get("type") or note.get("category") or "Update",
            "message": note.get("message") or note.get("title") or "",
            "timestamp": note.get("timestamp") or note.get("created_at") or "",
        }
        for note in notifications
    ]
