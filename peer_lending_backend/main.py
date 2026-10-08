from fastapi import FastAPI
from peer_lending_backend.src.routers.loans import router as loan_router
from peer_lending_backend.src.routers.collateral import router as collateral_router

app = FastAPI()

app.include_router(loan_router)
app.include_router(collateral_router)

@app.get("/health")
def health():
    return {"status": "ok"}
