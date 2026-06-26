from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from repositories.notification_template_repository import NotificationTemplateRepository
from services.notification_template_service import (
    INotificationTemplateService,
    NotificationTemplateService,
)


def get_notification_template_service(
    session: Session = Depends(get_session),
) -> INotificationTemplateService:
    notification_template_repository = NotificationTemplateRepository(session)

    return NotificationTemplateService(
        notification_template_repository=notification_template_repository,
    )