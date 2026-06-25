from abc import ABC, abstractmethod
from sqlmodel import Session, select

from app.models import NotificationTemplate, NotificationType


class INotificationTemplateRepository(ABC):
    @abstractmethod
    def get_by_type_and_channel(self, notification_type_id: int, channel_id: int) -> NotificationTemplate | None:
        pass

class NotificationTemplateRepository(INotificationTemplateRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_type_and_channel(
            self,
            notification_type_id: int,
            channel_id: int
    ) -> NotificationTemplate | None:
        statement = (select(NotificationTemplate)
                     .where(NotificationTemplate.notification_type_id == notification_type_id)
                     .where(NotificationTemplate.channel_id == channel_id)
                     )
        return self.session.exec(statement).first()