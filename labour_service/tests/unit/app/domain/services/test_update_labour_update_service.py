from copy import copy
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.exceptions import LabourUpdateNotFoundById
from src.labour.domain.labour.services.begin_labour import BeginLabourService
from src.labour.domain.labour_update.entity import LabourUpdate
from src.labour.domain.labour_update.enums import LabourUpdateType
from src.labour.domain.labour_update.exceptions import (
    CannotUpdateLabourUpdate,
    TooSoonSinceLastAnnouncement,
)
from src.labour.domain.labour_update.services.post_labour_update import PostLabourUpdateService
from src.labour.domain.labour_update.services.update_labour_update import UpdateLabourUpdateService
from src.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId


def get_user_generated_labour_update(labour: Labour) -> LabourUpdate:
    return next(update for update in labour.labour_updates if not update.application_generated)


def test_can_update_labour_update_message(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)  # 1 labour update is generated here
    labour = PostLabourUpdateService().post_labour_update(
        sample_labour, LabourUpdateType.STATUS_UPDATE, "Test"
    )
    assert len(labour.labour_updates) == 2
    labour_update = copy(get_user_generated_labour_update(labour))
    assert not labour_update.edited

    labour = UpdateLabourUpdateService().update_message(
        labour=labour, labour_update_id=labour_update.id_, message="New Message"
    )
    assert len(labour.labour_updates) == 2
    updated_labour_update = get_user_generated_labour_update(labour)
    assert updated_labour_update.edited
    assert labour_update.message != updated_labour_update.message


def test_cannot_update_labour_update_message_id_not_found(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)  # 1 labour update is generated here

    with pytest.raises(LabourUpdateNotFoundById):
        UpdateLabourUpdateService().update_message(
            labour=labour, labour_update_id=LabourUpdateId(uuid4()), message="New Message"
        )


def test_can_announce_labour_update(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)  # 1 labour update is generated here
    first_sent_time = datetime.now(UTC)
    labour = PostLabourUpdateService().post_labour_update(
        sample_labour, LabourUpdateType.STATUS_UPDATE, "Test", first_sent_time
    )
    assert len(labour.labour_updates) == 2
    labour_update = copy(get_user_generated_labour_update(labour))

    labour = UpdateLabourUpdateService().update_labour_type(
        labour=labour,
        labour_update_id=labour_update.id_,
        labour_update_type=LabourUpdateType.ANNOUNCEMENT,
    )
    assert len(labour.labour_updates) == 2
    updated_labour_update = get_user_generated_labour_update(labour)
    assert labour_update.labour_update_type != updated_labour_update.labour_update_type


def test_cannot_announce_an_announcement(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)  # 1 labour update is generated here
    first_sent_time = datetime.now(UTC)
    labour = PostLabourUpdateService().post_labour_update(
        sample_labour, LabourUpdateType.ANNOUNCEMENT, "Test", first_sent_time
    )
    labour_update = get_user_generated_labour_update(labour)

    with pytest.raises(CannotUpdateLabourUpdate):
        UpdateLabourUpdateService().update_labour_type(
            labour=labour,
            labour_update_id=labour_update.id_,
            labour_update_type=LabourUpdateType.ANNOUNCEMENT,
        )


def test_cannot_announce_labour_update_in_cooldown_period(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)  # 1 labour update is generated here
    first_sent_time = datetime.now(UTC)
    labour = PostLabourUpdateService().post_labour_update(
        sample_labour, LabourUpdateType.STATUS_UPDATE, "Test", first_sent_time
    )
    labour_update = get_user_generated_labour_update(labour)

    PostLabourUpdateService().post_labour_update(
        sample_labour, LabourUpdateType.ANNOUNCEMENT, "Test", first_sent_time
    )
    with pytest.raises(TooSoonSinceLastAnnouncement):
        UpdateLabourUpdateService().update_labour_type(
            labour=labour,
            labour_update_id=labour_update.id_,
            labour_update_type=LabourUpdateType.ANNOUNCEMENT,
        )


def test_cannot_update_application_generated_message(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)  # 1 labour update is generated here
    labour_update = labour.labour_updates[0]

    with pytest.raises(CannotUpdateLabourUpdate):
        UpdateLabourUpdateService().update_message(
            labour=labour,
            labour_update_id=labour_update.id_,
            message="test",
        )


def test_can_update_application_generated_type(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)  # 1 labour update is generated here
    labour_update = labour.labour_updates[0]

    labour = UpdateLabourUpdateService().update_labour_type(
        labour=labour,
        labour_update_id=labour_update.id_,
        labour_update_type=LabourUpdateType.ANNOUNCEMENT,
    )
