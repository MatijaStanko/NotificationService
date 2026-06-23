from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from repositories.notification_request_repository import NotificationRequestRepository
from app.schemas import NotificationCreate, NotificationResponse
from services.notification_service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification_data: NotificationCreate,
    session: Session = Depends(get_session)
):
    repository = NotificationRequestRepository(session)
    service = NotificationService(repository)

    notification = service.create_notification(notification_data)

    return NotificationResponse(
        id = notification.id,
        status=notification.status,
        channel = notification.channel,
        recipient = notification.recipient,
    )

@router.get("/")
def get_notifications():
    return {"message": "Notification router is working!"}