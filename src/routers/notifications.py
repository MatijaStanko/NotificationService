from fastapi import APIRouter, Depends, Body, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.models import NotificationRequest
from repositories.notification_request_repository import NotificationRequestRepository
from repositories.notification_template_repository import NotificationTemplateRepository
from repositories.notification_type_repository import NotificationTypeRepository
from repositories.channel_config_repository import ChannelConfigRepository
from services.notification_service import NotificationService
from services.notification_request_service import NotificationRequestService
from services.notification_template_service import NotificationTemplateService
from services.channel_config_service import ChannelConfigService
from services.notification_type_service import NotificationTypeService
from app.schemas import NotificationCreate, NotificationShortResponse, NotificationDetailedResponse

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.post("/", response_model=NotificationShortResponse)
def create_notification(
    notification_data: NotificationCreate= Body(
        example={
            "source_service": "user-service",
            "channel": "email",
            "notification_type": "welcome_user",
            "recipient": "matija@example.com",
            "template_data": {
                "first_name": "Matija",
                "activation_link": "https://example.com/activate/123"
            }
        }
    ),
    session: Session = Depends(get_session)
):
   notification_request_repository = NotificationRequestRepository(session)
   notification_type_repository = NotificationTypeRepository(session)
   channel_config_repository = ChannelConfigRepository(session)
   notification_template_repository = NotificationTemplateRepository(session)

   notification_request_service = NotificationRequestService(
       notification_request_repository = notification_request_repository
   )

   notification_template_service = NotificationTemplateService(
       notification_template_repository = notification_template_repository
   )

   notification_type_service = NotificationTypeService(
       notification_type_repository = notification_type_repository
   )

   channel_config_service = ChannelConfigService(
       channel_config_repository = channel_config_repository
   )

   notification_service = NotificationService(
       notification_request_service = notification_request_service,
       notification_type_service=notification_type_service,
       channel_config_service=channel_config_service,
       notification_template_service=notification_template_service,
   )

   try:
       notification = notification_service.create_notification(notification_data)
   except ValueError as error:
       raise HTTPException(status_code=400, detail=str(error))


   return NotificationShortResponse(
       id = notification.id,
       status = notification.status,
       channel=notification.channel,
       recipient=notification.recipient,
   )

@router.get(
    "/{notification_request_id}",
    response_model=NotificationDetailedResponse
)
def get_notification_request_by_id(
    notification_request_id: int,
    session: Session = Depends(get_session)
) -> NotificationDetailedResponse:

    notification_request_repository = NotificationRequestRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository = notification_request_repository
    )

    try:
        notification_request = notification_request_service.get_by_id(
            notification_request_id = notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return NotificationDetailedResponse(
        id=notification_request.id,
        source_service=notification_request.source_service,
        notification_type_id=notification_request.notification_type_id,
        template_id=notification_request.template_id,
        channel=notification_request.channel,
        recipient=notification_request.recipient,
        template_data=notification_request.template_data,
        rendered_subject=notification_request.rendered_subject,
        rendered_body=notification_request.rendered_body,
        status=notification_request.status,
        error_msg=notification_request.error_msg,
        created_at=notification_request.created_at,
        sent_at=notification_request.sent_at,
        updated_at=notification_request.updated_at,
    )




@router.get("/")
def get_notifications():
    return {"message": "Notification router is working!"}