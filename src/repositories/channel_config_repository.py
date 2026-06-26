from abc import ABC, abstractmethod
from sqlmodel import select, Session

from app.models import ChannelConfig

class IChannelConfigRepository(ABC):
    @abstractmethod
    def get_by_channel(self, channel: str) -> ChannelConfig | None:
        pass

    @abstractmethod
    def get_all(self) -> list[ChannelConfig]:
        pass

    @abstractmethod
    def get_by_id(self, channel_config_id: int) -> ChannelConfig | None:
        pass


class ChannelConfigRepository(IChannelConfigRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_channel(self, channel: str) -> ChannelConfig | None:
        statement = select(ChannelConfig).where(ChannelConfig.channel == channel)
        return self.session.exec(statement).first()

    def get_all(self) -> list[ChannelConfig]:
        statement = select(ChannelConfig).order_by(ChannelConfig.id)

        return list(self.session.exec(statement).all())

    def get_by_id(self, channel_config_id: int) -> ChannelConfig | None:
        return self.session.get(ChannelConfig, channel_config_id)