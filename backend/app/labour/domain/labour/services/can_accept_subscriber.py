from app.labour.domain.labour.constants import INNER_CIRCLE_MAX_SUBSCRIBERS
from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.labour.domain.labour.exceptions import (
    CannotSubscribeToOwnLabour,
    InsufficientLabourPaymentPlan,
    MaximumNumberOfSubscribersReached,
)
from app.user.domain.value_objects.user_id import UserId


class CanAcceptSubscriberService:
    def can_accept_subscriber(
        self, labour: Labour, subscriber_id: UserId, current_active_subscriptions: int
    ) -> None:
        if labour.birthing_person_id == subscriber_id:
            raise CannotSubscribeToOwnLabour()
        if labour.payment_plan == LabourPaymentPlan.INNER_CIRCLE.value:
            if current_active_subscriptions >= INNER_CIRCLE_MAX_SUBSCRIBERS:
                raise MaximumNumberOfSubscribersReached()
            return
        elif labour.payment_plan == LabourPaymentPlan.COMMUNITY.value:
            return
        else:
            raise InsufficientLabourPaymentPlan()
