from sqlmodel import Session

from app.models import NotificationRequest


class NotificationRequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, notification: NotificationRequest):
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification