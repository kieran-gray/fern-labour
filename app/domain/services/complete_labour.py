from datetime import UTC, datetime

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.entity import Labour
from app.domain.labour.exceptions import CannotCompleteLabourWithActiveContraction


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

        if active_labour.has_active_contraction:
            raise CannotCompleteLabourWithActiveContraction()

        active_labour.complete_labour(end_time=end_time or datetime.now(UTC), notes=notes)

        return active_labour
