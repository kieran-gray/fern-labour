import pytest

from app.labour.domain.labour.constants import INNER_CIRCLE_MAX_SUBSCRIBERS
from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.labour.domain.labour.exceptions import (
    CannotSubscribeToOwnLabour,
    InsufficientLabourPaymentPlan,
    MaximumNumberOfSubscribersReached,
)
from app.labour.domain.labour.services.can_accept_subscriber import CanAcceptSubscriberService
from app.user.domain.value_objects.user_id import UserId


def test_cannot_subscribe_to_own_labour(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    subscriber_id = sample_labour.birthing_person_id

    with pytest.raises(CannotSubscribeToOwnLabour):
        service.can_accept_subscriber(sample_labour, subscriber_id, current_active_subscriptions=0)


def test_maximum_number_of_subscribers_reached(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    sample_labour.payment_plan = LabourPaymentPlan.INNER_CIRCLE.value

    subscriber_id = UserId("subscriber")

    with pytest.raises(MaximumNumberOfSubscribersReached):
        service.can_accept_subscriber(
            sample_labour, subscriber_id, current_active_subscriptions=INNER_CIRCLE_MAX_SUBSCRIBERS
        )


def test_insufficient_labour_payment_plan_none(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    subscriber_id = UserId("subscriber")

    with pytest.raises(InsufficientLabourPaymentPlan):
        service.can_accept_subscriber(sample_labour, subscriber_id, current_active_subscriptions=0)


def test_insufficient_labour_payment_plan_solo(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    subscriber_id = UserId("subscriber")
    sample_labour.payment_plan = LabourPaymentPlan.SOLO.value

    with pytest.raises(InsufficientLabourPaymentPlan):
        service.can_accept_subscriber(sample_labour, subscriber_id, current_active_subscriptions=0)


def test_can_accept_subscriber_inner_circle(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    subscriber_id = UserId("subscriber")
    sample_labour.payment_plan = LabourPaymentPlan.INNER_CIRCLE.value

    service.can_accept_subscriber(
        sample_labour, subscriber_id, current_active_subscriptions=INNER_CIRCLE_MAX_SUBSCRIBERS - 1
    )


def test_can_accept_subscriber_community_plan(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    subscriber_id = UserId("subscriber")
    sample_labour.payment_plan = LabourPaymentPlan.COMMUNITY.value

    service.can_accept_subscriber(sample_labour, subscriber_id, current_active_subscriptions=100)
