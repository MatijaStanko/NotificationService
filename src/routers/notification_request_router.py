from fastapi import APIRouter, Body, Depends, HTTPException

from app.schemas import  NotificationCreate, NotificationDetailedResponse,  NotificationShortResponse

from app.dependencies import get_notification_request_service, get_notification_service
from services.notification_request_service import NotificationRequestService
from services.notification_service import NotificationService


router = APIRouter(
    prefix="/notifications",
    tags=["notification-requests"],
)


@router.post(
    "/",
    response_model=NotificationShortResponse,
    summary="Create notification request",
)
def create_notification(
    notification_data: NotificationCreate = Body(
        example={
            "source_service": "user-service",
            "channel": "email",
            "notification_type": "welcome_user",
            "recipient": "matija@example.com",
            "template_data": {
                "first_name": "Matija",
                "activation_link": "https://example.com/activate/123",
            },
        }
    ),
    notification_service : NotificationService = Depends(get_notification_service),
):
    try:
        notification_request = notification_service.create_notification(
            notification_data
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return notification_request


@router.get(
    "/{notification_request_id}",
    response_model=NotificationDetailedResponse,
    summary="Get notification request by ID",
)
def get_notification_request_by_id(
    notification_request_id: int,
    notification_request_service : NotificationRequestService= Depends(
        get_notification_request_service
    ),
):
    try:
        notification_request = notification_request_service.get_by_id(
            notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    return notification_request