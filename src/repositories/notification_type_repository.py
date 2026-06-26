from abc import ABC, abstractmethod
from sqlmodel import Session, select

from app.models import NotificationType

class INotificationTypeRepository(ABC):
    @abstractmethod
    def get_by_code(self, code: str) -> NotificationType | None:
        pass

    @abstractmethod
    def get_all(self) -> list[NotificationType]:
        pass

    @abstractmethod
    def get_by_id(self, notification_type_id: int) -> NotificationType | None:
        pass

class NotificationTypeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_code(self, code: str) -> NotificationType  | None:
        statement = select(NotificationType).where(NotificationType.code == code)
        return self.session.exec(statement).first()

    def get_all(self) -> list[NotificationType]:
        statement = select(NotificationType).order_by(NotificationType.id)

        return list(self.session.exec(statement).all())

    def get_by_id(self, notification_type_id: int) -> NotificationType | None:
        return self.session.get(NotificationType, notification_type_id)