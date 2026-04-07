from __future__ import annotations

from notification_platform.models.entities import Channel, DeliveryAttempt, DeliveryStatus, Notification


class PushProvider:
    name = "push-provider"

    def __init__(self, available: bool = True) -> None:
        self.available = available

    def send(self, notification: Notification) -> DeliveryAttempt:
        if not self.available:
            return DeliveryAttempt(
                notification_id=notification.notification_id,
                channel=Channel.PUSH,
                status=DeliveryStatus.FAILED,
                provider=self.name,
                details="Push provider unavailable",
            )

        return DeliveryAttempt(
            notification_id=notification.notification_id,
            channel=Channel.PUSH,
            status=DeliveryStatus.DELIVERED,
            provider=self.name,
            details="Push delivered",
        )
