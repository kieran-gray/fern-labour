from datetime import datetime

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.entity import Labour


class CompleteLabourService:
    def complete_labour(
        self,
        birthing_person: BirthingPerson,
        end_time: datetime | None = None,
        notes: str | None = None,
    ) -> Labour:
        active_labour = birthing_person.active_labour

        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person.id_)

        active_labour.complete_labour(end_time=end_time or datetime.now(), notes=notes)

        # TODO trigger domain event

        return active_labour
