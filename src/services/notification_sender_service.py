from app.models import NotificationRequest
from services.notification_request_service import NotificationRequestService
from services.channel_config_service import ChannelConfigService
from services.senders.email_sender import EmailSender

from abc import ABC, abstractmethod

class INotificationSenderService(ABC):
    class INotificationSenderService(ABC):
        @abstractmethod
        def send_notification(
                self,
                notification_request_id: int,
        ) -> NotificationRequest:
            pass

        @abstractmethod
        def process_pending_notifications(
                self,
                limit: int = 10,
        ) -> list[NotificationRequest]:
            pass


class NotificationSenderService(INotificationSenderService):
    def __init__(
            self,
            notification_request_service: NotificationRequestService,
            channel_config_service: ChannelConfigService,
            email_sender: EmailSender
    ):
        self.notification_request_service = notification_request_service
        self.channel_config_service = channel_config_service
        self.email_sender = email_sender

    def send_notification(self, notification_request_id: int) -> NotificationRequest:
        notification_request = self.notification_request_service.mark_as_processing(
            notification_request_id = notification_request_id
        )

        try:
            channel_config = self.channel_config_service.get_active_by_channel(
                channel=notification_request.channel
            )

            sender = self._get_sender(notification_request.channel)

            sender.send(
                notification_request=notification_request,
                channel_config=channel_config,
            )

            return self.notification_request_service.mark_as_sent(
                notification_request_id=notification_request_id
            )

        except Exception as error:
            return self.notification_request_service.mark_as_failed(
                notification_request_id=notification_request_id,
                error_msg=str(error)
            )

    def _get_sender(self, channel : str):
        if channel == "email":
            return self.email_sender

        raise ValueError(f"Unsupported notification channel: {channel}")

    def process_pending_notifications(self, limit: int = 10) -> list[NotificationRequest]:
        pending_notifications = self.notification_request_service.get_pending_requests(limit=limit)

        processed_notifications = []

        for notification_request in pending_notifications:
            processed_notification = self.send_notification(
                notification_request_id=notification_request.id
            )

            processed_notifications.append(processed_notification)

        return processed_notifications

