from fastapi import APIRouter, Depends, Query, HTTPException

from app.schemas import NotificationDetailedResponse, NotificationFailedRequest
from app.dependencies import get_notification_request_service, get_notification_sender_service
from services.notification_request_service import NotificationRequestService
from services.notification_sender_service import NotificationSenderService


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)

@router.get(
    "/pending",
    response_model=list[NotificationDetailedResponse],
    summary="Get pending notification requests",
)
def get_pending_notification_requests(
    limit: int = Query(default=10, ge=1, le=100),
    notification_request_service: NotificationRequestService = Depends(
        get_notification_request_service
    ),
):
    return notification_request_service.get_pending_requests(limit)

@router.post(
    "/proces-pending",
    response_model = list[NotificationDetailedResponse]
)
def process_pending_notification_requests(
        limit: int = Query(default=10, ge=1, le=100),
        notification_sender_service: NotificationSenderService = Depends(get_notification_sender_service)
):
    return notification_sender_service.process_pending_notifications(limit=limit)
@router.patch(
    "/{notification_request_id}/processing",
    response_model=NotificationDetailedResponse,
    summary="Mark notification request as processing",
)
def mark_notification_request_as_processing(
    notification_request_id: int,
    notification_request_service: NotificationRequestService = Depends(
        get_notification_request_service
    ),
):
    try:
        notification_request = notification_request_service.mark_as_processing(
            notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return notification_request

@router.patch(
    "/{notification_request_id}/sent",
    response_model=NotificationDetailedResponse,
    summary="Mark notification request as sent",
)
def mark_notification_request_as_sent(
    notification_request_id: int,
    notification_request_service: NotificationRequestService = Depends(
        get_notification_request_service
    ),
):
    try:
        notification_request = notification_request_service.mark_as_sent(
            notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return notification_request


@router.patch(
    "/{notification_request_id}/failed",
    response_model=NotificationDetailedResponse,
    summary="Mark notification request as failed",
)
def mark_notification_request_as_failed(
    notification_request_id: int,
    failed_request: NotificationFailedRequest,
    notification_request_service: NotificationRequestService = Depends(
        get_notification_request_service
    ),
):
    try:
        notification_request = notification_request_service.mark_as_failed(
            notification_request_id=notification_request_id,
            error_msg=failed_request.error_msg,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return notification_request


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