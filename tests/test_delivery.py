from notification_platform.models.entities import Channel, DeliveryStatus, Notification, NotificationType, UserPreferences
from notification_platform.providers.email import EmailProvider
from notification_platform.providers.push import PushProvider
from notification_platform.providers.sms import SmsProvider
from notification_platform.services.delivery import DeliveryService


def build_service(push_available: bool, sms_available: bool, email_available: bool) -> DeliveryService:
    return DeliveryService(
        providers={
            Channel.PUSH: PushProvider(available=push_available),
            Channel.SMS: SmsProvider(available=sms_available),
            Channel.EMAIL: EmailProvider(available=email_available),
        }
    )


def test_transactional_notification_falls_back_to_sms() -> None:
    service = build_service(push_available=False, sms_available=True, email_available=True)

    notification = Notification(
        notification_id="n-1",
        user_id="u-1",
        notification_type=NotificationType.TRANSACTIONAL,
        title="Transfer confirmed",
        body="Your transfer was completed",
        channels_priority=[Channel.PUSH, Channel.SMS, Channel.EMAIL],
    )

    preferences = UserPreferences(
        user_id="u-1",
        allow_marketing=False,
        allow_service=True,
        preferred_channels=[Channel.PUSH, Channel.SMS, Channel.EMAIL],
    )

    attempts = service.deliver(notification, preferences)

    assert len(attempts) == 2
    assert attempts[0].channel == Channel.PUSH
    assert attempts[0].status == DeliveryStatus.FAILED
    assert attempts[1].channel == Channel.SMS
    assert attempts[1].status == DeliveryStatus.DELIVERED


def test_marketing_notification_can_be_disabled() -> None:
    service = build_service(push_available=True, sms_available=True, email_available=True)

    notification = Notification(
        notification_id="n-2",
        user_id="u-1",
        notification_type=NotificationType.MARKETING,
        title="Special offer",
        body="Get cashback this week",
        channels_priority=[Channel.PUSH, Channel.EMAIL],
    )

    preferences = UserPreferences(
        user_id="u-1",
        allow_marketing=False,
        allow_service=True,
        preferred_channels=[Channel.PUSH, Channel.EMAIL],
    )

    attempts = service.deliver(notification, preferences)

    assert len(attempts) == 1
    assert attempts[0].status == DeliveryStatus.SKIPPED


def test_duplicate_notification_is_prevented() -> None:
    service = build_service(push_available=True, sms_available=True, email_available=True)

    notification = Notification(
        notification_id="n-3",
        user_id="u-1",
        notification_type=NotificationType.TRANSACTIONAL,
        title="Debit",
        body="Money was debited",
        channels_priority=[Channel.PUSH, Channel.SMS],
    )

    preferences = UserPreferences(
        user_id="u-1",
        allow_marketing=True,
        allow_service=True,
        preferred_channels=[Channel.PUSH, Channel.SMS],
    )

    first_attempts = service.deliver(notification, preferences)
    second_attempts = service.deliver(notification, preferences)

    assert first_attempts[-1].status == DeliveryStatus.DELIVERED
    assert second_attempts[0].status == DeliveryStatus.SKIPPED
