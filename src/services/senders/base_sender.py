from abc import ABC, abstractmethod

from app.models import NotificationRequest, ChannelConfig

class BaseSender(ABC):
    @abstractmethod
    def send(
            self,
            notification_request: NotificationRequest,
            channel_config: ChannelConfig
    ) -> None:
        pass