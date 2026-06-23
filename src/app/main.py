from fastapi import FastAPI

from app.config import settings
from routers import notifications
app = FastAPI(
    title = settings.app_name,
    version = settings.app_version,
    debug = settings.debug
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service" : settings.app_name,
        "version" : settings.app_version
    }

app.include_router(notifications.router)