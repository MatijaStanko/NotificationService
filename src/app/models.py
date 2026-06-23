from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB

class NotificationType(SQLModel, table=True):
    __tablename__ = "notification_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    code : str = Field(index=True, unique=True)
    is_active : bool = True

class NotificationTemplate(SQLModel, table=True):
    __tablename__ = "notification_templates"

    id: Optional[int] = Field(default=None, primary_key=True)
    notification_type_id : int = Field(foreign_key="notification_types.id")
    channel_id : int = Field(foreign_key="channel_configs.id", index=True)
    subject_template: Optional[str] = None
    body_template: str
    required_variables: dict = Field(default_factory=dict, sa_column=Column(JSONB))
    is_active: bool = True

class ChannelConfig(SQLModel, table=True):
    __tablename__ = "channel_configs"

    id: Optional[int] = Field(default=None, primary_key=True)
    channel: str = Field(index=True, unique=True)
    provider: str
    config : dict = Field(default_factory=dict, sa_column=Column(JSONB))
    is_active: bool = True

class NotificationRequest(SQLModel, table=True):
    __tablename__ = "notification_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    source_service: Optional[str] = None
    notification_type_id: int = Field(foreign_key="notification_types.id")
    template_id: Optional[int] = Field(default=None, foreign_key="notification_templates.id", nullable=True)
    channel: str = Field(index=True)
    recipient: str = Field(index=True)
    template_data: dict = Field(default_factory=dict, sa_column=Column(JSONB))
    rendered_subject: Optional[str] = None
    rendered_body: Optional[str] = None
    status: str = Field(index=True, default='pending')
    error_msg: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
