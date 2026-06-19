from src.api import app
__all__ = ["app"]
from src.api import app
__all__ = ["app"]
from api import notifications, payback

app.include_router(notifications.router)
app.include_router(payback.router)
