from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas import NotificationDetailedResponse
from repositories.notification_request_repository import NotificationRequestRepository
from services.notification_request_service import NotificationRequestService

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
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
        NotificationDetailedResponse(
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
        for notification_request in pending_requests
    ]
