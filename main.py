from src.api import app
from src.api.payback import router as payback_router

app.include_router(payback_router)

__all__ = ["app"]
from api import payback, notifications
app.include_router(payback.router)
app.include_router(notifications.router)
