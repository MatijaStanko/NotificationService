from app.models import NotificationRequest
from repositories.notification_request_repository import NotificationRequestRepository
from app.schemas import NotificationCreate

class NotificationService:
    def __init__(self, repository: NotificationRequestRepository):
        self.repository = repository

    def create_notification(self, data : NotificationCreate) -> NotificationRequest:
        notification = NotificationRequest(
            source_service = data.source_service,
            channel = data.channel,
            recipient = data.recipient,
            template_data = data.template_data,
            status = "pending",

            notification_type_id = 1,
            template_id = None
        )

        return self.repository.create(notification)