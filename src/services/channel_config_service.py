from abc import ABC, abstractmethod
from app.models import ChannelConfig
from repositories.channel_config_repository import ChannelConfigRepository

class IChannelConfigService(ABC):
    @abstractmethod
    def get_active_by_channel(self, channel: str) -> ChannelConfig:
        pass

class ChannelConfigService(IChannelConfigService):
    def __init__(self, channel_config_repository: ChannelConfigRepository):
        self.channel_config_repository = channel_config_repository

    def get_active_by_channel(self, channel: str) -> ChannelConfig:
        chanel_config = self.channel_config_repository.get_by_channel(channel)

        if chanel_config is None:
            raise ValueError("Channel does not exist")

        if not chanel_config.is_active:
            raise ValueError("Channel is inactive")

        return chanel_config
