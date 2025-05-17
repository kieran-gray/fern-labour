from fern_labour_core.exceptions.domain import DomainError

from src.labour.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS


class TooSoonSinceLastAnnouncement(DomainError):
    def __init__(self) -> None:
        super().__init__(
            f"Wait at least {ANNOUNCEMENT_COOLDOWN_SECONDS} seconds between announcements"
        )


class CannotUpdateAnnouncement(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot update an announcement")
