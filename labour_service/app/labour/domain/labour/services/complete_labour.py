from datetime import UTC, datetime

from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.enums import LabourPhase
from app.labour.domain.labour.exceptions import (
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

        return labour
