
from fastapi import FastAPI

from peer_lending_backend.src.auth.auth import router as auth_router
from peer_lending_backend.src.routers.collateral import router as collateral_router
from peer_lending_backend.src.routers.credit import router as credit_router
from peer_lending_backend.src.routers.identity import router as identity_router
from peer_lending_backend.src.routers.loans import router as loans_router

app = FastAPI(
    title="Pulse Lending API",
    version="0.1.0",
    description="Unified backend for Accesso Ancla + Pulse Lending"
)

app.include_router(auth_router)
app.include_router(identity_router, prefix="/identity", tags=["Identity"])
app.include_router(collateral_router, prefix="/collateral", tags=["Collateral"])
app.include_router(credit_router, prefix="/credit", tags=["Credit"])
app.include_router(loans_router, prefix="/loan", tags=["Loan"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Pulse Lending API running"}
