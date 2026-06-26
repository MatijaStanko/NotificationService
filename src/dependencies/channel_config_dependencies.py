from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from repositories.channel_config_repository import ChannelConfigRepository
from services.channel_config_service import (
    ChannelConfigService,
    IChannelConfigService,
)


def get_channel_config_service(
    session: Session = Depends(get_session),
) -> IChannelConfigService:
    channel_config_repository = ChannelConfigRepository(session)

    return ChannelConfigService(
        channel_config_repository=channel_config_repository,
    )