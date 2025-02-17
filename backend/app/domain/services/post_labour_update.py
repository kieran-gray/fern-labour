from datetime import UTC, datetime, timedelta

from app.domain.labour.entity import Labour
from app.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from app.domain.labour_update.enums import LabourUpdateType
from app.domain.labour_update.exceptions import TooSoonSinceLastAnnouncement


class PostLabourUpdateService:
    def post_labour_update(
        self,
        labour: Labour,
        labour_update_type: LabourUpdateType,
        message: str,
        sent_time: datetime | None = None,
    ) -> Labour:
        if labour_update_type is LabourUpdateType.ANNOUNCEMENT and labour.announcements:
            most_recent_announcement = labour.announcements[-1]
            if datetime.now(UTC) - most_recent_announcement.sent_time < timedelta(
                seconds=ANNOUNCEMENT_COOLDOWN_SECONDS
            ):
                raise TooSoonSinceLastAnnouncement()

        labour.add_labour_update(
            labour_update_type=labour_update_type, message=message, sent_time=sent_time
        )

        return labour
