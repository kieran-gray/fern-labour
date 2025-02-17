from datetime import datetime

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour


class PlanLabourService:
    def plan_labour(
        self,
        birthing_person_id: BirthingPersonId,
        first_labour: bool,
        due_date: datetime,
        labour_name: str | None = None,
    ) -> Labour:
        labour = Labour.plan(
            birthing_person_id=birthing_person_id,
            first_labour=first_labour,
            due_date=due_date,
            labour_name=labour_name,
        )
        return labour
