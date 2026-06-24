from sqlmodel import Session, select

from app.models import NotificationType

class NotificationTypeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_code(self, code: str) -> NotificationType  | None:
        statement = select(NotificationType).where(NotificationType.code == code)
        return self.session.exec(statement).first()
