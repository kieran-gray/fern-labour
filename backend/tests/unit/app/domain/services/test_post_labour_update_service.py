from datetime import UTC, datetime, timedelta

import pytest

from app.domain.labour_update.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from app.domain.labour_update.exceptions import TooSoonSinceLastAnnouncement
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.post_labour_update import PostLabourUpdateService
from app.domain.labour_update.enums import LabourUpdateType


def test_can_post_labour_update(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    PostLabourUpdateService().post_labour_update(sample_birthing_person, LabourUpdateType.ANNOUNCEMENT, "Test")


def test_cannot_post_labour_update_without_active_labour(sample_birthing_person: BirthingPerson):
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        PostLabourUpdateService().post_labour_update(sample_birthing_person, LabourUpdateType.ANNOUNCEMENT, "Test")


def test_cannot_post_labour_update_in_cooldown_period(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    first_sent_time = datetime.now(UTC)
    within_cooldown_period = first_sent_time + timedelta(seconds=ANNOUNCEMENT_COOLDOWN_SECONDS - 1)
    PostLabourUpdateService().post_labour_update(sample_birthing_person, LabourUpdateType.ANNOUNCEMENT, "Test", first_sent_time)
    with pytest.raises(TooSoonSinceLastAnnouncement):
        PostLabourUpdateService().post_labour_update(
            sample_birthing_person, LabourUpdateType.ANNOUNCEMENT, "Test", within_cooldown_period
        )


def test_can_post_labour_update_outside_cooldown_period(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    first_sent_time = datetime.now(UTC)
    within_cooldown_period = first_sent_time + timedelta(seconds=ANNOUNCEMENT_COOLDOWN_SECONDS)
    PostLabourUpdateService().post_labour_update(sample_birthing_person, LabourUpdateType.ANNOUNCEMENT, "Test", first_sent_time)
    with pytest.raises(TooSoonSinceLastAnnouncement):
        PostLabourUpdateService().post_labour_update(
            sample_birthing_person, LabourUpdateType.ANNOUNCEMENT, "Test", within_cooldown_period
        )
