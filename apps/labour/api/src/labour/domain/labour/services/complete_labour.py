from datetime import UTC, datetime

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.events import LabourCompleted
from src.labour.domain.labour.exceptions import (
    CannotCompleteLabourWithActiveContraction,
    LabourAlreadyCompleted,
)


class CompleteLabourService:
    def complete_labour(
        self,
        labour: Labour,
        end_time: datetime | None = None,
        notes: str | None = None,
    ) -> Labour:
        if labour.current_phase is LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()

        if labour.has_active_contraction:
            raise CannotCompleteLabourWithActiveContraction()

        labour.complete_labour(end_time=end_time or datetime.now(UTC), notes=notes)

        labour.add_domain_event(LabourCompleted.from_domain(labour=labour))

        return labour
