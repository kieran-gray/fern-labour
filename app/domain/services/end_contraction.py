from datetime import datetime

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.entity import Labour
from app.domain.labour.exceptions import LabourHasNoActiveContraction


class EndContractionService:
    def end_contraction(
        self,
        birthing_person: BirthingPerson,
        intensity: int | None = None,
        end_time: datetime | None = None,
        notes: str | None = None,
    ) -> Labour:
        active_labour = birthing_person.active_labour

        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person.id_)

        if not active_labour.has_active_contraction:
            raise LabourHasNoActiveContraction()

        active_labour.end_contraction(
            intensity=intensity, end_time=end_time or datetime.now(), notes=notes
        )

        # TODO trigger domain event

        return active_labour
