from sqlmodel import Session, select

from app.models import NotificationRequest


class NotificationRequestRepository:
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

