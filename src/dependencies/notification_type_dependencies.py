from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from repositories.notification_type_repository import NotificationTypeRepository
from services.notification_type_service import (
    INotificationTypeService,
    NotificationTypeService,
)


def get_notification_type_service(
    session: Session = Depends(get_session),
) -> INotificationTypeService:
    notification_type_repository = NotificationTypeRepository(session)

    return NotificationTypeService(
        notification_type_repository=notification_type_repository,
    )