from datetime import UTC, datetime

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.exceptions import LabourHasNoActiveContraction
from src.labour.domain.labour.services.update_labour_phase import UpdateLabourPhaseService


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
