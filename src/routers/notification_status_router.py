from fastapi import APIRouter, Depends, HTTPException

from app.schemas import NotificationDetailedResponse, NotificationFailedRequest
from dependencies.notification_request_dependencies import (
    get_notification_request_service,
)
from services.notification_request_service import NotificationRequestService


router = APIRouter(
    prefix="/notifications",
    tags=["notification-status"],
)


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