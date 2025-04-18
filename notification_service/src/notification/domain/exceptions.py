from src.common.domain.exceptions import DomainError, DomainValidationError


class InvalidNotificationType(DomainValidationError):
    def __init__(self, notification_type: str | None) -> None:
        super().__init__(f"Notification type '{notification_type}' is not valid.")


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


class NotificationProcessingError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class GenerationTemplateNotFound(DomainError):
    def __init__(self, template: str) -> None:
        super().__init__(f"Notification generation template not found for template '{template}'.")


class InvalidNotificationTemplate(DomainValidationError):
    def __init__(self, template: str | None) -> None:
        super().__init__(f"Notification template '{template}' is not valid.")
