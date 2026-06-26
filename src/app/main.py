from contextlib import asynccontextmanager

from fastapi import FastAPI


from app.config import settings
from app.db_seed import seed_database
from routers import (
    notification_request_router,
    notification_sending_router,
    notification_status_router,
    channel_config_router,
    notification_type_router,
    notification_template_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_database()
    yield
app = FastAPI(
    title = settings.app_name,
    version = settings.app_version,
    debug = settings.debug,
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service" : settings.app_name,
        "version" : settings.app_version
    }

app.include_router(notification_type_router.router)
app.include_router(channel_config_router.router)
app.include_router(notification_template_router.router)
app.include_router(notification_sending_router.router)
app.include_router(notification_status_router.router)
app.include_router(notification_request_router.router)
