from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas import NotificationDetailedResponse
from dependencies.notification_sending_dependencies import get_notification_sender_service
from services.notification_sender_service import NotificationSenderService


router = APIRouter(
    prefix="/notifications",
    tags=["notification-sending"],
)


@router.post(
    "/{notification_request_id}/send",
    response_model=NotificationDetailedResponse,
    summary="Send notification request",
)
def send_notification_request(
    notification_request_id: int,
    notification_sender_service: NotificationSenderService = Depends(
        get_notification_sender_service
    ),
):
    try:
        notification_request = notification_sender_service.send_notification(
            notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return notification_request


@router.post(
    "/process-pending",
    response_model=list[NotificationDetailedResponse],
    summary="Process pending notification requests",
)
def process_pending_notification_requests(
    limit: int = Query(default=10, ge=1, le=100),
    notification_sender_service: NotificationSenderService = Depends(
        get_notification_sender_service
    ),
):
    return notification_sender_service.process_pending_notifications(limit)