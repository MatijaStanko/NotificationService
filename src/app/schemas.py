from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, ConfigDict


class NotificationCreate(BaseModel):
    source_service: str | None = None
    channel: str
    notification_type: str
    recipient: str
    template_data: dict[str, Any] = {}

class NotificationShortResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    channel: str
    recipient: str

class NotificationDetailedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_service: str | None
    notification_type_id: int
    template_id: int | None
    channel: str
    recipient: str
    template_data: dict[str, Any]
    rendered_subject: str | None
    rendered_body: str | None
    status: str
    error_msg: str | None
    created_at: datetime
    sent_at: datetime | None
    updated_at: datetime

class NotificationFailedRequest(BaseModel):
    error_msg: str

class DeleteAllNotificationRequestsResponse(BaseModel):
    deleted_count: int

class NotificationTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    is_active: bool


class ChannelConfigResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    channel: str
    provider: str
    config: dict
    is_active: bool


class NotificationTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    notification_type_id: int
    channel_id: int
    subject_template: str | None
    body_template: str
    required_variables: dict
    is_active: bool
