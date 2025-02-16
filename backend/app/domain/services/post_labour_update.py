from datetime import UTC, datetime, timedelta

from app.domain.labour_update.enums import LabourUpdateType
from app.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from app.domain.labour_update.exceptions import TooSoonSinceLastAnnouncement
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.entity import Labour
from app.domain.birthing_person.entity import BirthingPerson


class PostLabourUpdateService:
    def post_labour_update(
        self,
        birthing_person: BirthingPerson,
        labour_update_type: LabourUpdateType,
        message: str,
        sent_time: datetime | None = None,
    ) -> Labour:
        active_labour = birthing_person.active_labour

        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person.id_)

        if labour_update_type is LabourUpdateType.ANNOUNCEMENT and active_labour.announcements:
            most_recent_announcement = active_labour.announcements[-1]
            if datetime.now(UTC) - most_recent_announcement.sent_time < timedelta(
                seconds=ANNOUNCEMENT_COOLDOWN_SECONDS
            ):
                raise TooSoonSinceLastAnnouncement()

        active_labour.add_labour_update(
            labour_update_type=labour_update_type,
            message=message,
            sent_time=sent_time
        )

        return active_labour
