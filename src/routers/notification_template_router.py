from fastapi import APIRouter, Depends, HTTPException

from app.schemas import NotificationTemplateResponse
from dependencies.notification_template_dependencies import (
    get_notification_template_service,
)
from services.notification_template_service import INotificationTemplateService


router = APIRouter(
    prefix="/notification-templates",
    tags=["notification-templates"],
)


@router.get(
    "/",
    response_model=list[NotificationTemplateResponse],
    summary="Get all notification templates",
)
def get_notification_templates(
    notification_template_service: INotificationTemplateService = Depends(
        get_notification_template_service
    ),
):
    return notification_template_service.get_all()


@router.get(
    "/{notification_template_id}",
    response_model=NotificationTemplateResponse,
    summary="Get notification template by ID",
)
def get_notification_template_by_id(
    notification_template_id: int,
    notification_template_service: INotificationTemplateService = Depends(
        get_notification_template_service
    ),
):
    try:
        return notification_template_service.get_by_id(notification_template_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))