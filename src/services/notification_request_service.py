from abc import ABC, abstractmethod
from app.models import NotificationRequest
from repositories.notification_request_repository import NotificationRequestRepository

class INotificationRequestService(ABC):
    @abstractmethod
    def create(self, notification_request: NotificationRequest) -> NotificationRequest:
        pass

    @abstractmethod
    def get_by_id(self, notification_request_id: int) -> type[NotificationRequest]:
        pass

    @abstractmethod
    def get_pending_requests(self, limit: int) -> type[NotificationRequest]:
        pass

    @abstractmethod
    def mark_as_processing(self, notification_request: NotificationRequest) -> NotificationRequest:
        pass

    @abstractmethod
    def mark_as_sent(self, notification_request_id: int) -> NotificationRequest:
        pass

    @abstractmethod
    def mark_as_failed(self, notification_request_id: int, error_msg: str) -> NotificationRequest:
        pass

    @abstractmethod
    def delete_by_id(self, notification_request_id: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> int:
        pass

class NotificationRequestService(INotificationRequestService):
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

    def get_pending_requests(self, limit: int = 10) -> list[NotificationRequest]:
        return self.notification_request_repository.get_pending_request(limit)

    def mark_as_processing(self, notification_request_id: int) -> NotificationRequest:
        notification_request = self.get_by_id(notification_request_id)

        if notification_request.status != "pending":
            raise ValueError("Only pending notification requests can be marked as processing")

        return self.notification_request_repository.mark_as_processing(notification_request)

    def mark_as_sent(self, notification_request_id: int) -> NotificationRequest:
        notification_request = self.get_by_id(notification_request_id)

        if notification_request.status != "processing":
            raise ValueError("Only proccesing notification requests can be marked as sent")

        return self.notification_request_repository.mark_as_sent(notification_request)

    def mark_as_failed(
            self,
            notification_request_id: int,
            error_msg: str
    ) -> NotificationRequest:
        notification_request = self.get_by_id(notification_request_id)

        if notification_request.status != "processing":
            raise ValueError("Only processing notification requests can be marked as failed")

        return self.notification_request_repository.mark_as_failed(
            notification_request = notification_request,
            error_msg = error_msg
        )

    def delete_by_id(self, notification_request_id: int) -> None:
        notification_request = self.get_by_id(notification_request_id)

        self.notification_request_repository.delete_by_id(notification_request)

    def delete_all(self) -> int:
        return self.notification_request_repository.delete_all()