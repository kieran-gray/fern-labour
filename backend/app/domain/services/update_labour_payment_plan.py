from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPaymentPlan, LabourPhase
from app.domain.labour.exceptions import (
    CannotDowngradeLabourPlan,
    LabourAlreadyCompleted,
)


class UpdateLabourPaymentPlanService:
    labour_payment_plan_order = [
        LabourPaymentPlan.SOLO,
        LabourPaymentPlan.INNER_CIRCLE,
        LabourPaymentPlan.COMMUNITY,
    ]

    def update_payment_plan(self, labour: Labour, payment_plan: LabourPaymentPlan) -> Labour:
        if labour.current_phase is LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()

        if labour.payment_plan and self.labour_payment_plan_order.index(
            payment_plan
        ) < self.labour_payment_plan_order.index(labour.payment_plan):
            raise CannotDowngradeLabourPlan()

        labour.update_payment_plan(payment_plan=payment_plan)

        return labour
