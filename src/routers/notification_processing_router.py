from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas import NotificationDetailedResponse, NotificationFailedRequest
from repositories.notification_request_repository import NotificationRequestRepository
from repositories.channel_config_repository import ChannelConfigRepository
from services.notification_request_service import NotificationRequestService
from services.channel_config_service import ChannelConfigService
from services.notification_sender_service import NotificationSenderService
from services.senders.email_sender import EmailSender

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)

def map_to_detailed_response(notification_request) -> NotificationDetailedResponse:
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

@router.get("/pending", response_model= list[NotificationDetailedResponse])
def get_pending_notification_requests(
        limit: int = Query(10, ge=1, le=100),
        session: Session = Depends(get_session)
):
    notification_request_repository = NotificationRequestRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository=notification_request_repository
    )

    pending_requests = notification_request_service.get_pending_requests(limit)

    return [
        map_to_detailed_response(notification_request)
        for notification_request in pending_requests
    ]

@router.post(
    "/{notification_request_id}/processing",
    response_model= NotificationDetailedResponse
)
def mark_notification_request_as_processing(
        notification_request_id: int,
        session: Session = Depends(get_session)
):
    notification_request_repository = NotificationRequestRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository = notification_request_repository
    )

    try:
        notification_request = notification_request_service.mark_as_processing(
            notification_request_id=notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return map_to_detailed_response(notification_request)

@router.post(
    "/{notification_request_id}/sent",
    response_model=NotificationDetailedResponse,
    summary="Mark notification request as sent",
)
def mark_notification_request_as_sent(
    notification_request_id: int,
    session: Session = Depends(get_session),
):
    notification_request_repository = NotificationRequestRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository=notification_request_repository,
    )

    try:
        notification_request = notification_request_service.mark_as_sent(
            notification_request_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return map_to_detailed_response(notification_request)

@router.post(
    "/{notification_request_id}/failed",
    response_model=NotificationDetailedResponse,
    summary="Mark notification request as failed",
)
def mark_notification_request_as_failed(
    notification_request_id: int,
    failed_request: NotificationFailedRequest,
    session: Session = Depends(get_session),
):
    notification_request_repository = NotificationRequestRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository=notification_request_repository,
    )

    try:
        notification_request = notification_request_service.mark_as_failed(
            notification_request_id=notification_request_id,
            error_msg=failed_request.error_msg,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return map_to_detailed_response(notification_request)

@router.post(
    "/{notification_request_id}/send",
    response_model=NotificationDetailedResponse
)
def send_notification_request(
    notification_request_id: int,
    session: Session = Depends(get_session),
):
    notification_request_repository = NotificationRequestRepository(session)
    channel_config_repository = ChannelConfigRepository(session)

    notification_request_service = NotificationRequestService(
        notification_request_repository=notification_request_repository,
    )

    channel_config_service = ChannelConfigService(
        channel_config_repository=channel_config_repository,
    )

    email_sender = EmailSender()

    notification_sender_service = NotificationSenderService(
        notification_request_service=notification_request_service,
        channel_config_service=channel_config_service,
        email_sender=email_sender,
    )

    notification_request = notification_sender_service.send_notification(
        notification_request_id
    )

    return map_to_detailed_response(notification_request)