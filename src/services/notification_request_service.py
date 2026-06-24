from app.models import NotificationRequest
from repositories.notification_request_repository import NotificationRequestRepository

class NotificationRequestService:
    def __init__(self, notification_request_repository: NotificationRequestRepository):
        self.notification_request_repository = notification_request_repository

    def create(
            self,
            notification_request: NotificationRequest
    ) -> NotificationRequest:
        return self.notification_request_repository.create(notification_request)