from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional

from src.api.loans import router as loans_router
from src.api.notifications import router as notifications_router
from src.api.payback import router as payback_router

app = FastAPI(title="Peer Lending API", version="1.0.0")

# -------------------------------
# 🔹 Pydantic Schemas
# -------------------------------

class ErrorResponse(BaseModel):
    code: int
    message: str
    details: Optional[str] = None

class AuthRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    token: str
    user_id: int

class ScoringRequest(BaseModel):
    borrower_id: int
    loan_amount: float
    credit_score: int

class ScoringResponse(BaseModel):
    borrower_id: int
    risk_tier: str
    probability_of_default: float

class PaybackStatusRequest(BaseModel):
    loan_id: int

class PaybackStatusResponse(BaseModel):
    loan_id: int
    status: str
    next_due_date: Optional[str]

class IntegrationHookRequest(BaseModel):
    provider: str  # "stripe" or "plaid"
    payload: dict

class IntegrationHookResponse(BaseModel):
    success: bool
    message: str

# -------------------------------
# 🔹 Endpoints
# -------------------------------

@app.post("/api/v1/auth/login", response_model=AuthResponse, responses={400: {"model": ErrorResponse}})
def login(request: AuthRequest):
    if request.email == "test@example.com" and request.password == "password":
        return AuthResponse(token="fake-jwt-token", user_id=1)
    raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/api/v1/auth/signup", response_model=AuthResponse, responses={400: {"model": ErrorResponse}})
def signup(request: AuthRequest):
    # TODO: Save user to DB
    return AuthResponse(token="new-user-token", user_id=2)

@app.post("/api/v1/scoring", response_model=ScoringResponse, responses={400: {"model": ErrorResponse}})
def scoring(request: ScoringRequest):
    # Simple demo scoring logic
    if request.credit_score >= 700:
        tier, pd = "Low", 0.05
    elif request.credit_score >= 600:
        tier, pd = "Medium", 0.15
    else:
        tier, pd = "High", 0.35
    return ScoringResponse(borrower_id=request.borrower_id, risk_tier=tier, probability_of_default=pd)

@app.post("/api/v1/payback_status", response_model=PaybackStatusResponse, responses={404: {"model": ErrorResponse}})
def payback_status(request: PaybackStatusRequest):
    # Demo: pretend loan_id=1 is active
    if request.loan_id == 1:
        return PaybackStatusResponse(loan_id=1, status="Active", next_due_date="2026-07-01")
    raise HTTPException(status_code=404, detail="Loan not found")

@app.post("/api/v1/integration_hooks", response_model=IntegrationHookResponse, responses={400: {"model": ErrorResponse}})
def integration_hooks(request: IntegrationHookRequest):
    if request.provider not in ["stripe", "plaid"]:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    # TODO: process webhook payload
    return IntegrationHookResponse(success=True, message=f"Processed {request.provider} payload")


app.include_router(payback_router)
app.include_router(loans_router)
app.include_router(notifications_router)
