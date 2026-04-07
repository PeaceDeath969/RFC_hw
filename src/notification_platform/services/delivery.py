from __future__ import annotations

from typing import Dict, List, Set

from notification_platform.models.entities import (
    Channel,
    DeliveryAttempt,
    DeliveryStatus,
    Notification,
    NotificationType,
    UserPreferences,
)


class DeliveryService:
    def __init__(self, providers: Dict[Channel, object]) -> None:
        self.providers = providers
        self.processed_ids: Set[str] = set()

    def _is_allowed_by_preferences(
        self,
        notification: Notification,
        preferences: UserPreferences,
    ) -> bool:
        if notification.notification_type == NotificationType.MARKETING:
            return preferences.allow_marketing

        if notification.notification_type == NotificationType.SERVICE:
            return preferences.allow_service

        return True

    def _resolve_channels(
        self,
        notification: Notification,
        preferences: UserPreferences,
    ) -> List[Channel]:
        preferred = [ch for ch in preferences.preferred_channels if ch in notification.channels_priority]
        remaining = [ch for ch in notification.channels_priority if ch not in preferred]
        return preferred + remaining

    def deliver(
        self,
        notification: Notification,
        preferences: UserPreferences,
    ) -> List[DeliveryAttempt]:
        if notification.notification_id in self.processed_ids:
            return [
                DeliveryAttempt(
                    notification_id=notification.notification_id,
                    channel=notification.channels_priority[0],
                    status=DeliveryStatus.SKIPPED,
                    provider="deduplication",
                    details="Duplicate notification prevented",
                )
            ]

        if not self._is_allowed_by_preferences(notification, preferences):
            return [
                DeliveryAttempt(
                    notification_id=notification.notification_id,
                    channel=notification.channels_priority[0],
                    status=DeliveryStatus.SKIPPED,
                    provider="preferences",
                    details="Notification disabled by user preferences",
                )
            ]

        attempts: List[DeliveryAttempt] = []
        channels = self._resolve_channels(notification, preferences)

        for channel in channels:
            provider = self.providers[channel]
            attempt = provider.send(notification)
            attempts.append(attempt)

            if attempt.status == DeliveryStatus.DELIVERED:
                self.processed_ids.add(notification.notification_id)
                break

        return attempts
