from datetime import UTC, datetime

from app.domain.labour.entity import Labour
from app.domain.labour.exceptions import LabourHasNoActiveContraction
from app.domain.services.update_labour_phase import UpdateLabourPhaseService


class EndContractionService:
    def end_contraction(
        self,
        labour: Labour,
        intensity: int,
        end_time: datetime | None = None,
        notes: str | None = None,
    ) -> Labour:
        if not labour.has_active_contraction:
            raise LabourHasNoActiveContraction()

        labour.end_contraction(
            intensity=intensity, end_time=end_time or datetime.now(UTC), notes=notes
        )

        labour = UpdateLabourPhaseService().update_labour_phase(labour)

        return labour
