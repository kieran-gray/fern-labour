from app.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from app.domain.base.exceptions import DomainError


class TooSoonSinceLastAnnouncement(DomainError):
    def __init__(self) -> None:
        super().__init__(
            f"Wait at least {ANNOUNCEMENT_COOLDOWN_SECONDS} seconds between announcements"
        )
