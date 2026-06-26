from abc import ABC, abstractmethod

from app.models import NotificationRequest
from app.schemas import NotificationCreate
from services import notification_service
from services.notification_sender_service import NotificationSenderService
from services.notification_service import NotificationService

class INotificationOrchestrationService(ABC):
    @abstractmethod
    def create_and_send_notification(
            self,
            notification_data : NotificationCreate,
    ) -> NotificationRequest:
        pass


class NotificationOrchestrationService(INotificationOrchestrationService):
    def __init__(
            self,
            notification_service : NotificationService,
            notification_sender_service : NotificationSenderService,
    ):
        self.notification_service = notification_service
        self.notification_sender_service = notification_sender_service

    def create_and_send_notification(
            self,
            notification_data : NotificationCreate
    ) -> NotificationRequest:
        notification_request = self.notification_service.create_notification(
            data = notification_data
        )

        return self.notification_sender_service.send_notification(
            notification_request_id=notification_request.id
        )
