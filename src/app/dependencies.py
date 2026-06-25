from fastapi import Depends
from sqlmodel import Session

from app.database import get_session

from repositories.channel_config_repository import ChannelConfigRepository
from repositories.notification_request_repository import NotificationRequestRepository
from repositories.notification_template_repository import NotificationTemplateRepository
from repositories.notification_type_repository import NotificationTypeRepository

from services.channel_config_service import ChannelConfigService
from services.notification_request_service import NotificationRequestService
from services.notification_service import NotificationService
from services.notification_sender_service import NotificationSenderService
from services.notification_template_service import NotificationTemplateService
from services.notification_type_service import NotificationTypeService
from services.senders.email_sender import EmailSender
from services.senders.sender_factory import SenderFactory

def get_notification_request_service(
    session: Session = Depends(get_session)
) -> NotificationRequestService:
    notification_request_repository = NotificationRequestRepository(session)

    return NotificationRequestService(
        notification_request_repository=notification_request_repository,
    )

def get_notification_service(
    session: Session = Depends(get_session),
) -> NotificationService:
    notification_request_repository = NotificationRequestRepository(session)
    notification_type_repository = NotificationTypeRepository(session)
    channel_config_repository = ChannelConfigRepository(session)
    notification_template_repository = NotificationTemplateRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository=notification_request_repository
    )

    notification_type_service = NotificationTypeService(
        notification_type_repository=notification_type_repository
    )

    channel_config_service = ChannelConfigService(
        channel_config_repository=channel_config_repository
    )

    notification_template_service = NotificationTemplateService(
        notification_template_repository=notification_template_repository
    )

    return NotificationService(
        notification_request_service=notification_request_service,
        notification_type_service=notification_type_service,
        channel_config_service=channel_config_service,
        notification_template_service=notification_template_service
    )

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

    sender_factory = SenderFactory(
        email_sender=email_sender,
    )

    return NotificationSenderService(
        notification_request_service=notification_request_service,
        channel_config_service=channel_config_service,
        sender_factory=sender_factory,
    )
