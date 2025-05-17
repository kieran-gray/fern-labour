from datetime import UTC, datetime, timedelta

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.events import LabourUpdatePosted
from src.labour.domain.labour.exceptions import LabourUpdateNotFoundById
from src.labour.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from src.labour.domain.labour_update.entity import LabourUpdate
from src.labour.domain.labour_update.enums import LabourUpdateType
from src.labour.domain.labour_update.exceptions import (
    CannotUpdateAnnouncement,
    TooSoonSinceLastAnnouncement,
)
from src.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId


class UpdateLabourUpdateService:
    def _get_labour_update(self, labour: Labour, labour_update_id: LabourUpdateId) -> LabourUpdate:
        for labour_update in labour.labour_updates:
            if labour_update.id_ == labour_update_id:
                return labour_update
        raise LabourUpdateNotFoundById(labour_update_id=labour_update_id)

    def update_labour_type(
        self,
        labour: Labour,
        labour_update_id: LabourUpdateId,
        labour_update_type: LabourUpdateType,
    ) -> Labour:
        labour_update = self._get_labour_update(labour=labour, labour_update_id=labour_update_id)
        if labour_update.labour_update_type is LabourUpdateType.ANNOUNCEMENT:
            raise CannotUpdateAnnouncement()

        if labour_update_type is LabourUpdateType.ANNOUNCEMENT and labour.announcements:
            most_recent_announcement = labour.announcements[-1]
            if datetime.now(UTC) - most_recent_announcement.sent_time < timedelta(
                seconds=ANNOUNCEMENT_COOLDOWN_SECONDS
            ):
                raise TooSoonSinceLastAnnouncement()

        labour_update.update(labour_update_type=labour_update_type)

        labour.add_domain_event(
            LabourUpdatePosted.create(
                {
                    "birthing_person_id": labour.birthing_person_id.value,
                    "labour_id": str(labour.id_.value),
                    "labour_update_type": labour_update_type.value,
                    "labour_update_id": str(labour_update.id_.value),
                    "message": labour_update.message,
                    "sent_time": labour_update.sent_time.isoformat(),
                }
            )
        )
        return labour

    def update_message(
        self,
        labour: Labour,
        labour_update_id: LabourUpdateId,
        message: str,
    ) -> Labour:
        labour_update = self._get_labour_update(labour=labour, labour_update_id=labour_update_id)
        labour_update.update(message=message)

        return labour
