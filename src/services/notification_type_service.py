from app.models import NotificationType
from repositories.notification_type_repository import NotificationTypeRepository


class NotificationTypeService:
    def __init__(self, notification_type_repository: NotificationTypeRepository):
        self.notification_type_repository = notification_type_repository


    def get_active_by_code(self, code: str) -> NotificationType:
        notification_type = self.notification_type_repository.get_by_code(code)

        if notification_type is None:
            raise ValueError("Notification type does not exists")

        if not notification_type.is_active:
            raise ValueError("Notification type is inactive")

        return notification_type
