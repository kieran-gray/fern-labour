from app.domain.base.exceptions import DomainError, DomainValidationError


class InvalidNotificationStatus(DomainValidationError):
    def __init__(self, notification_status: str | None) -> None:
        super().__init__(f"Notification status '{notification_status}' is not valid.")


class InvalidNotificationId(DomainValidationError):
    def __init__(self, notification_id: str | None) -> None:
        super().__init__(f"Notification id '{notification_id}' is not valid.")


class NotificationNotFoundById(DomainError):
    def __init__(self, notification_id: str | None) -> None:
        super().__init__(f"Notification with id '{notification_id}' not found.")


class NotificationNotFoundByExternalId(DomainError):
    def __init__(self, external_id: str | None) -> None:
        super().__init__(f"Notification with external id '{external_id}' not found.")
