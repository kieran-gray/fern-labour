from datetime import UTC, datetime

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.exceptions import LabourAlreadyCompleted, LabourHasActiveContraction


class StartContractionService:
    def start_contraction(
        self,
        labour: Labour,
        intensity: int | None = None,
        start_time: datetime | None = None,
        notes: str | None = None,
    ) -> Labour:
        if labour.has_active_contraction:
            raise LabourHasActiveContraction()

        if labour.current_phase == LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()

        labour.start_contraction(
            intensity=intensity, start_time=start_time or datetime.now(UTC), notes=notes
        )

        return labour
