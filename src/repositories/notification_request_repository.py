from abc import ABC, abstractmethod
from datetime import datetime
from sqlmodel import Session, select

from app.models import NotificationRequest

class INotificationRequestRepository(ABC):

    @abstractmethod
    def create(self, notificationReq: NotificationRequest):
        pass

    @abstractmethod
    def get_by_id(self, notification_request_id: int) -> type[NotificationRequest] | None:
        pass

    @abstractmethod
    def get_pending_request(self, limit: int = 10) -> list[NotificationRequest]:
        pass

    @abstractmethod
    def mark_as_processing(self, notification_request: NotificationRequest) -> NotificationRequest:
        pass

    @abstractmethod
    def mark_as_sent(self, notification_request: NotificationRequest) -> NotificationRequest:
        pass

    @abstractmethod
    def mark_as_failed(self, notification_request: NotificationRequest, error_msg: str) -> NotificationRequest:
        pass

    @abstractmethod
    def delete_by_id(self, notification_request_id: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> int:
        pass

class NotificationRequestRepository(INotificationRequestRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, notificationReq: NotificationRequest):
        self.session.add(notificationReq)
        self.session.commit()
        self.session.refresh(notificationReq)
        return notificationReq

    def get_by_id(self, notification_request_id: int) -> type[NotificationRequest] | None:
        return self.session.get(NotificationRequest, notification_request_id)

    def get_pending_request(self, limit: int = 10) -> list[NotificationRequest]:
        statement = (
            select(NotificationRequest)
            .where(NotificationRequest.status == "pending")
            .order_by(NotificationRequest.created_at)
            .limit(limit)
        )

        return list(self.session.exec(statement).all())

    def mark_as_processing(self, notification_request: NotificationRequest) -> NotificationRequest:
        notification_request.status = "processing"
        notification_request.updated_at = datetime.utcnow()

        self.session.add(notification_request)
        self.session.commit()
        self.session.refresh(notification_request)

        return notification_request

    def mark_as_sent(self, notification_request: NotificationRequest) -> NotificationRequest:
        notification_request.status = "sent"
        notification_request.sent_at = datetime.utcnow()
        notification_request.updated_at = datetime.utcnow()
        notification_request.error_msg = None

        self.session.add(notification_request)
        self.session.commit()
        self.session.refresh(notification_request)

        return notification_request

    def mark_as_failed(
            self,
            notification_request: NotificationRequest,
            error_msg: str
    ) -> NotificationRequest:
        notification_request.status = "failed"
        notification_request.error_msg = error_msg
        notification_request.updated_at = datetime.utcnow()

        self.session.add(notification_request)
        self.session.commit()
        self.session.refresh(notification_request)

        return notification_request

    def delete_by_id(self, notification_request: NotificationRequest) -> None:
        self.session.delete(notification_request)
        self.session.commit()


    def delete_all(self) -> int:
        notification_requests = self.session.exec(
            select(NotificationRequest)
        ).all()

        deleted_count = len(notification_requests)

        for notification_request in notification_requests:
            self.session.delete(notification_request)

        self.session.commit()

        return deleted_count