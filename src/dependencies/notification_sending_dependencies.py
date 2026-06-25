from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from repositories.channel_config_repository import ChannelConfigRepository
from repositories.notification_request_repository import NotificationRequestRepository
from services.channel_config_service import ChannelConfigService
from services.notification_request_service import NotificationRequestService
from services.notification_sender_service import NotificationSenderService
from services.senders.email_sender import EmailSender


def get_notification_sender_service(
    session: Session = Depends(get_session),
) -> NotificationSenderService:
    notification_request_repository = NotificationRequestRepository(session)
    channel_config_repository = ChannelConfigRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository=notification_request_repository,
    )

    channel_config_service = ChannelConfigService(
        channel_config_repository=channel_config_repository,
    )

    email_sender = EmailSender()

    return NotificationSenderService(
        notification_request_service=notification_request_service,
        channel_config_service=channel_config_service,
        email_sender=email_sender,
    )