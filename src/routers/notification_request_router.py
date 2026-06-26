from fastapi import APIRouter, Body, Depends, Query, HTTPException

from app.schemas import  NotificationCreate, NotificationDetailedResponse, DeleteAllNotificationRequestsResponse

from dependencies.notification_request_dependencies import get_notification_request_service, get_notification_orchestration_service
from services.notification_request_service import NotificationRequestService
from services.notification_orchestration_service import NotificationOrchestrationService


router = APIRouter(
    prefix="/notifications",
    tags=["notification-requests"],
)


@router.post(
    "/",
    response_model=NotificationDetailedResponse,
    summary="Create and send notification request",
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
    notification_orchestration_service: NotificationOrchestrationService = Depends(get_notification_orchestration_service),
):
    try:
        notification_request = notification_orchestration_service.create_and_send_notification(
            notification_data = notification_data
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return notification_request

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

@router.delete(
    "/{notification_request_id}",
    status_code=204,
    summary="Delete notification request by ID"
)
def delete_notification_request_by_id(
        notification_request_id: int,
        notification_request_service : NotificationRequestService= Depends(
            get_notification_request_service
        )
):
    try:
        notification_request_service.delete_by_id(
            notification_request_id = notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.delete(
    "/",
    response_model=DeleteAllNotificationRequestsResponse,
    summary="Delete all notification requests",
)
def delete_all_notification_requests(
    notification_request_service: NotificationRequestService = Depends(
        get_notification_request_service
    ),
):
    deleted_count = notification_request_service.delete_all()

    return DeleteAllNotificationRequestsResponse(
        deleted_count=deleted_count,
    )