from sqlmodel import Session

from app.models import NotificationRequest


class NotificationRequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, notificationReq: NotificationRequest):
        self.session.add(notificationReq)
        self.session.commit()
        self.session.refresh(notificationReq)
        return notificationReq