from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from peer_lending_backend.src.supabase_client import supabase

router = APIRouter(prefix="/api/collateral", tags=["collateral"])


class CollateralCreate(BaseModel):
    loan_id: int
    description: str
    value: float = Field(gt=0)


@router.get("")
def list_collateral(loan_id: int | None = Query(default=None)):
    query = supabase.table("collateral").select("*")
    if loan_id is not None:
        query = query.eq("loan_id", loan_id)
    return query.execute().data or []


@router.get("/{collateral_id}")
def get_collateral(collateral_id: int):
    response = supabase.table("collateral").select("*").eq("id", collateral_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Collateral not found")
    return response.data[0]


@router.post("", status_code=201)
def create_collateral(item: CollateralCreate):
    response = supabase.table("collateral").insert(item.model_dump()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Collateral not created")
    return response.data[0]
