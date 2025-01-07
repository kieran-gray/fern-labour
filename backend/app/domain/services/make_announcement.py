from datetime import UTC, datetime, timedelta

from app.domain.announcement.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from app.domain.announcement.exceptions import TooSoonSinceLastAnnouncement
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.entity import Labour


class MakeAnnouncementService:
    def make_announcement(
        self,
        birthing_person: BirthingPerson,
        message: str,
        sent_time: datetime | None = None,
    ) -> Labour:
        active_labour = birthing_person.active_labour

        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person.id_)

        if active_labour.announcements:
            most_recent_announcement = active_labour.announcements[-1]
            if datetime.now(UTC) - most_recent_announcement.sent_time < timedelta(
                seconds=ANNOUNCEMENT_COOLDOWN_SECONDS
            ):
                raise TooSoonSinceLastAnnouncement()

        active_labour.add_announcement(message=message, sent_time=sent_time)

        return active_labour
