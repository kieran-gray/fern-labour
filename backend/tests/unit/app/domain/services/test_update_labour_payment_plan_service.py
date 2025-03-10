import pytest

from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPaymentPlan
from app.domain.labour.exceptions import CannotDowngradeLabourPlan, LabourAlreadyCompleted
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.complete_labour import CompleteLabourService
from app.domain.services.update_labour_payment_plan import UpdateLabourPaymentPlanService


@pytest.mark.parametrize(
    "payment_plan",
    [LabourPaymentPlan.SOLO, LabourPaymentPlan.INNER_CIRCLE, LabourPaymentPlan.COMMUNITY],
)
def test_can_update_labour_payment_plan(sample_labour: Labour, payment_plan: LabourPaymentPlan):
    assert sample_labour.payment_plan is None
    labour = UpdateLabourPaymentPlanService().update_payment_plan(
        labour=sample_labour, payment_plan=payment_plan
    )
    assert labour.payment_plan == payment_plan


@pytest.mark.parametrize(
    "start_payment_plan,downgrade_payment_plans",
    [
        (LabourPaymentPlan.INNER_CIRCLE, [LabourPaymentPlan.SOLO]),
        (
            LabourPaymentPlan.COMMUNITY,
            [LabourPaymentPlan.INNER_CIRCLE, LabourPaymentPlan.SOLO],
        ),
    ],
)
def test_cannot_downgrade_labour_payment_plan(
    sample_labour: Labour,
    start_payment_plan: LabourPaymentPlan,
    downgrade_payment_plans: list[LabourPaymentPlan],
):
    assert sample_labour.payment_plan is None
    labour = UpdateLabourPaymentPlanService().update_payment_plan(
        labour=sample_labour, payment_plan=start_payment_plan
    )
    assert labour.payment_plan == start_payment_plan

    for payment_plan in downgrade_payment_plans:
        with pytest.raises(CannotDowngradeLabourPlan):
            UpdateLabourPaymentPlanService().update_payment_plan(
                labour=labour, payment_plan=payment_plan
            )


def test_cannot_update_labour_payment_plan_of_completed_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    CompleteLabourService().complete_labour(sample_labour)
    with pytest.raises(LabourAlreadyCompleted):
        UpdateLabourPaymentPlanService().update_payment_plan(
            labour=sample_labour, payment_plan=LabourPaymentPlan.SOLO
        )
