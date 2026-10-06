from src.api import app

__all__ = ["app"]

from routers import loans, users, collateral, repayments

app.include_router(loans.router)
app.include_router(users.router)
app.include_router(collateral.router)
app.include_router(repayments.router)
