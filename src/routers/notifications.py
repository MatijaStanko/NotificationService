from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from repositories.notification_request_repository import NotificationRequestRepository
from repositories.notification_template_repository import NotificationTemplateRepository
from repositories.notification_type_repository import NotificationTypeRepository
from repositories.channel_config_repository import ChannelConfigRepository
from services.notification_service import NotificationService
from services.notification_request_service import NotificationRequestService
from services.notification_template_service import NotificationTemplateService
from services.channel_config_service import ChannelConfigService
from services.notification_type_service import NotificationTypeService
from app.schemas import NotificationCreate, NotificationResponse

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification_data: NotificationCreate,
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


   return NotificationResponse(
       id = notification.id,
       status = notification.status,
       channel=notification.channel,
       recipient=notification.recipient,
   )

@router.get("/")
def get_notifications():
    return {"message": "Notification router is working!"}