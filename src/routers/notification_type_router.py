from fastapi import APIRouter, Depends, HTTPException

from app.schemas import NotificationTypeResponse
from dependencies.notification_type_dependencies import (
    get_notification_type_service,
)
from services.notification_type_service import INotificationTypeService


router = APIRouter(
    prefix="/notification-types",
    tags=["notification-types"],
)


@router.get(
    "/",
    response_model=list[NotificationTypeResponse],
    summary="Get all notification types",
)
def get_notification_types(
    notification_type_service: INotificationTypeService = Depends(
        get_notification_type_service
    ),
):
    return notification_type_service.get_all()


@router.get(
    "/{notification_type_id}",
    response_model=NotificationTypeResponse,
    summary="Get notification type by ID",
)
def get_notification_type_by_id(
    notification_type_id: int,
    notification_type_service: INotificationTypeService = Depends(
        get_notification_type_service
    ),
):
    try:
        return notification_type_service.get_by_id(notification_type_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))