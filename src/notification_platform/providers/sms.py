from __future__ import annotations

from notification_platform.models.entities import Channel, DeliveryAttempt, DeliveryStatus, Notification


class SmsProvider:
    name = "sms-provider"

    def __init__(self, available: bool = True) -> None:
        self.available = available

    def send(self, notification: Notification) -> DeliveryAttempt:
        if not self.available:
            return DeliveryAttempt(
                notification_id=notification.notification_id,
                channel=Channel.SMS,
                status=DeliveryStatus.FAILED,
                provider=self.name,
                details="SMS provider unavailable",
            )

        return DeliveryAttempt(
            notification_id=notification.notification_id,
            channel=Channel.SMS,
            status=DeliveryStatus.DELIVERED,
            provider=self.name,
            details="SMS delivered",
        )
