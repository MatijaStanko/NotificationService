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

    def get_by_id(self, notification_request_id: int) -> type[NotificationRequest]:
        notification_request = self.notification_request_repository.get_by_id(notification_request_id)

        if notification_request is None:
            raise ValueError("Notification request does not exists")

        return notification_request
