from fastapi import APIRouter, Depends, HTTPException

from app.schemas import ChannelConfigResponse
from dependencies.channel_config_dependencies import (
    get_channel_config_service,
)
from services.channel_config_service import IChannelConfigService


router = APIRouter(
    prefix="/channel-configs",
    tags=["channel-configs"],
)


@router.get(
    "/",
    response_model=list[ChannelConfigResponse],
    summary="Get all channel configs",
)
def get_channel_configs(
    channel_config_service: IChannelConfigService = Depends(
        get_channel_config_service
    ),
):
    return channel_config_service.get_all()


@router.get(
    "/{channel_config_id}",
    response_model=ChannelConfigResponse,
    summary="Get channel config by ID",
)
def get_channel_config_by_id(
    channel_config_id: int,
    channel_config_service: IChannelConfigService = Depends(
        get_channel_config_service
    ),
):
    try:
        return channel_config_service.get_by_id(channel_config_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))