from fastapi import FastAPI
from peer_lending_backend.src.routers.loans import router as loan_router
from peer_lending_backend.src.routers.collateral import router as collateral_router

app = FastAPI()

app.include_router(loan_router)
app.include_router(collateral_router)

@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import FastAPI
from routers.loans import router as loans_router
from routers.collateral import router as collateral_router
from routers.identity import router as identity_router
from routers.credit import router as credit_router

app = FastAPI(
    title="Pulse Lending API",
    version="0.1.0",
    description="Unified backend for Accesso Ancla + Pulse Lending"
)

# --- Route Groups ---
app.include_router(identity_router, prefix="/identity", tags=["Identity"])
app.include_router(collateral_router, prefix="/collateral", tags=["Collateral"])
app.include_router(credit_router, prefix="/credit", tags=["Credit"])
app.include_router(loans_router, prefix="/loan", tags=["Loan"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Pulse Lending API running"}
