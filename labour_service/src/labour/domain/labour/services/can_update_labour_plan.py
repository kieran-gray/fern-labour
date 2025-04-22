from src.labour.domain.labour.constants import LABOUR_PAYMENT_PLAN_ORDER
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPaymentPlan, LabourPhase
from src.labour.domain.labour.exceptions import (
    CannotDowngradeLabourPlan,
    LabourAlreadyCompleted,
)


class CanUpdateLabourPlanService:
    def can_update_labour_plan(self, labour: Labour, payment_plan: LabourPaymentPlan) -> bool:
        if labour.current_phase is LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()

        if labour.payment_plan and LABOUR_PAYMENT_PLAN_ORDER.index(
            payment_plan
        ) < LABOUR_PAYMENT_PLAN_ORDER.index(labour.payment_plan):
            raise CannotDowngradeLabourPlan()

        return True
