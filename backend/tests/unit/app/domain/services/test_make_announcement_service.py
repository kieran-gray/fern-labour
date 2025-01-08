from datetime import UTC, datetime, timedelta

import pytest

from app.domain.announcement.constants import ANNOUNCEMENT_COOLDOWN_SECONDS
from app.domain.announcement.exceptions import TooSoonSinceLastAnnouncement
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.make_announcement import MakeAnnouncementService


def test_can_make_announcement(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    MakeAnnouncementService().make_announcement(sample_birthing_person, "Test")


def test_cannot_make_announcement_without_active_labour(sample_birthing_person: BirthingPerson):
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        MakeAnnouncementService().make_announcement(sample_birthing_person, "Test")


def test_cannot_make_announcement_in_cooldown_period(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    first_sent_time = datetime.now(UTC)
    within_cooldown_period = first_sent_time + timedelta(seconds=ANNOUNCEMENT_COOLDOWN_SECONDS - 1)
    MakeAnnouncementService().make_announcement(sample_birthing_person, "Test", first_sent_time)
    with pytest.raises(TooSoonSinceLastAnnouncement):
        MakeAnnouncementService().make_announcement(
            sample_birthing_person, "Test", within_cooldown_period
        )


def test_can_make_announcement_outside_cooldown_period(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    first_sent_time = datetime.now(UTC)
    within_cooldown_period = first_sent_time + timedelta(seconds=ANNOUNCEMENT_COOLDOWN_SECONDS)
    MakeAnnouncementService().make_announcement(sample_birthing_person, "Test", first_sent_time)
    with pytest.raises(TooSoonSinceLastAnnouncement):
        MakeAnnouncementService().make_announcement(
            sample_birthing_person, "Test", within_cooldown_period
        )
