from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr

class NotificationCreate(BaseModel):
    source_service: str | None = None
    channel: str
    notification_type: str
    recipient: EmailStr
    template_data: dict[str, Any] = {}

class NotificationShortResponse(BaseModel):
    id: int
    status: str
    channel: str
    recipient: str

class NotificationDetailedResponse(BaseModel):
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
