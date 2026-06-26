from abc import ABC, abstractmethod
from sqlmodel import Session, select

from app.models import NotificationTemplate, NotificationType, ChannelConfig


class INotificationTemplateRepository(ABC):
    @abstractmethod
    def get_by_type_and_channel(self, notification_type_id: int, channel_id: int) -> NotificationTemplate | None:
        pass

    @abstractmethod
    def get_all(self) -> list[NotificationTemplate]:
        pass

    @abstractmethod
    def get_by_id(self, notification_type_id: int) -> NotificationTemplate | None:
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
        return self.session.exec(statement).one_or_none()

    def get_all(self) -> list[NotificationTemplate]:
        statement = select(NotificationTemplate).order_by(NotificationTemplate.id)

        return list(self.session.exec(statement).all())

    def get_by_id(self, notification_template_id: int) -> NotificationTemplate | None:
        return self.session.get(NotificationTemplate, notification_template_id)