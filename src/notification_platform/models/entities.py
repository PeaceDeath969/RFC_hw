from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    TRANSACTIONAL = "transactional"
    SERVICE = "service"
    MARKETING = "marketing"


class Channel(str, Enum):
    PUSH = "push"
    SMS = "sms"
    EMAIL = "email"


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    SKIPPED = "skipped"


class UserPreferences(BaseModel):
    user_id: str
    allow_marketing: bool = True
    allow_service: bool = True
    preferred_channels: List[Channel] = Field(
        default_factory=lambda: [Channel.PUSH, Channel.SMS, Channel.EMAIL]
    )


class Notification(BaseModel):
    notification_id: str
    user_id: str
    notification_type: NotificationType
    title: str
    body: str
    channels_priority: List[Channel]


class DeliveryAttempt(BaseModel):
    notification_id: str
    channel: Channel
    status: DeliveryStatus
    provider: str
    details: Optional[str] = None
