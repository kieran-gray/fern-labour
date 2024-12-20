from datetime import datetime

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import LabourCompleted, LabourHasActiveContraction


class StartContractionService:

    def start_contraction(
        self,
        birthing_person: BirthingPerson,
        intensity: int,
        start_time: datetime | None = None,
        notes: str | None = None
    ) -> Labour:
        active_labour = birthing_person.active_labour

        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person.id_)

        if active_labour.has_active_contraction:
            raise LabourHasActiveContraction()

        if active_labour.current_phase == LabourPhase.COMPLETE:
            raise LabourCompleted()

        active_labour.start_contraction(
            intensity=intensity,
            start_time=start_time or datetime.now(),
            notes=notes
        )

        # TODO trigger domain event

        return active_labour
