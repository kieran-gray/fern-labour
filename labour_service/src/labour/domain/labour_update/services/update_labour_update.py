from datetime import UTC, datetime, timedelta

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.events import LabourBegun, LabourUpdatePosted
from src.labour.domain.labour.exceptions import LabourUpdateNotFoundById
from src.labour.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from src.labour.domain.labour_update.entity import LabourUpdate
from src.labour.domain.labour_update.enums import LabourUpdateType
from src.labour.domain.labour_update.exceptions import (
    CannotUpdateLabourUpdate,
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
            raise CannotUpdateLabourUpdate()

        if labour_update_type is LabourUpdateType.ANNOUNCEMENT and labour.announcements:
            most_recent_announcement = labour.announcements[-1]
            if datetime.now(UTC) - most_recent_announcement.sent_time < timedelta(
                seconds=ANNOUNCEMENT_COOLDOWN_SECONDS
            ):
                raise TooSoonSinceLastAnnouncement()

        labour_update.update(labour_update_type=labour_update_type)

        if (
            labour_update.application_generated
            and labour_update_type is LabourUpdateType.ANNOUNCEMENT
        ):
            if labour_update.message == "labour_begun":
                labour.add_domain_event(LabourBegun.from_domain(labour=labour))
        else:
            labour.add_domain_event(
                LabourUpdatePosted.from_domain(labour=labour, labour_update=labour_update)
            )
        return labour

    def update_message(
        self,
        labour: Labour,
        labour_update_id: LabourUpdateId,
        message: str,
    ) -> Labour:
        labour_update = self._get_labour_update(labour=labour, labour_update_id=labour_update_id)
        if labour_update.application_generated:
            raise CannotUpdateLabourUpdate()

        labour_update.update(message=message)

        return labour
