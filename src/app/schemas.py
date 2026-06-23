from typing import Any

from pydantic import BaseModel, EmailStr

class NotificationCreate(BaseModel):
    source_service: str | None = None
    channel: str
    notification_type: str
    recipient: EmailStr
    template_data: dict[str, Any] = {}

class NotificationResponse(BaseModel):
    id: int
    status: str
    channel: str
    recipient: str

