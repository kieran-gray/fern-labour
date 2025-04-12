from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.labour.domain.labour.services.can_update_labour_plan import CanUpdateLabourPlanService


class UpdateLabourPaymentPlanService:
    def update_payment_plan(self, labour: Labour, payment_plan: LabourPaymentPlan) -> Labour:
        CanUpdateLabourPlanService().can_update_labour_plan(
            labour=labour, payment_plan=payment_plan
        )
        labour.update_payment_plan(payment_plan=payment_plan)

        return labour
