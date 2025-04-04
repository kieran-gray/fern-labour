from app.domain.base.exceptions import DomainError
from app.labour.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS


class TooSoonSinceLastAnnouncement(DomainError):
    def __init__(self) -> None:
        super().__init__(
            f"Wait at least {ANNOUNCEMENT_COOLDOWN_SECONDS} seconds between announcements"
        )
