from abc import ABC, abstractmethod
from sqlmodel import select, Session

from app.models import ChannelConfig

class IChannelConfigRepository(ABC):
    @abstractmethod
    def get_by_channel(self, channel: str) -> ChannelConfig | None:
        pass


class ChannelConfigRepository(IChannelConfigRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_channel(self, channel: str) -> ChannelConfig | None:
        statement = select(ChannelConfig).where(ChannelConfig.channel == channel)
        return self.session.exec(statement).first()
