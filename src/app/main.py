from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models
from app.config import settings
from app.database import create_db_and_tables
from routers import notification_request_router, notification_processing_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
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

app.include_router(notification_processing_router.router)
app.include_router(notification_request_router.router)
