from datetime import datetime
from uuid import UUID

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.events import LabourPlanned
from src.user.domain.value_objects.user_id import UserId


class PlanLabourService:
    def plan_labour(
        self,
        birthing_person_id: UserId,
        first_labour: bool,
        due_date: datetime,
        labour_name: str | None = None,
        labour_id: UUID | None = None,
    ) -> Labour:
        labour = Labour.plan(
            birthing_person_id=birthing_person_id,
            first_labour=first_labour,
            due_date=due_date,
            labour_name=labour_name,
            labour_id=labour_id,
        )

        labour.add_domain_event(LabourPlanned.from_domain(labour=labour))

        return labour
