from fastapi import FastAPI

from app import models
from app.config import settings
from app.database import create_db_and_tables
from routers import notification_request_router
app = FastAPI(
    title = settings.app_name,
    version = settings.app_version,
    debug = settings.debug
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service" : settings.app_name,
        "version" : settings.app_version
    }

app.include_router(notification_request_router.router)