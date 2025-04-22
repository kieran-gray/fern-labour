import itertools
from datetime import datetime

from src.labour.domain.contraction.exceptions import (
    CannotUpdateActiveContraction,
    ContractionNotFoundById,
    ContractionsOverlappingAfterUpdate,
)
from src.labour.domain.contraction.value_objects.contraction_duration import Duration
from src.labour.domain.contraction.value_objects.contraction_id import ContractionId
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.exceptions import LabourAlreadyCompleted


class UpdateContractionService:
    def update_contraction(
        self,
        labour: Labour,
        contraction_id: ContractionId,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        intensity: int | None = None,
        notes: str | None = None,
    ) -> Labour:
        if labour.current_phase == LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()

        contraction = next(
            (
                contraction
                for contraction in labour.contractions
                if contraction.id_ == contraction_id
            ),
            None,
        )
        if not contraction:
            raise ContractionNotFoundById(contraction_id=contraction_id.value)

        if contraction.is_active:
            raise CannotUpdateActiveContraction()

        if start_time and end_time:
            contraction.update_duration(start_time=start_time, end_time=end_time)
        elif start_time:
            contraction.update_start_time(start_time=start_time)
        elif end_time:
            contraction.update_end_time(end_time=end_time)

        if start_time or end_time:
            if self._check_for_overlapping_contraction_durations(labour=labour):
                raise ContractionsOverlappingAfterUpdate()

        if intensity:
            contraction.update_intensity(intensity=intensity)

        if notes:
            contraction.add_notes(notes=notes)

        return labour

    def _check_for_overlapping_contraction_durations(self, labour: Labour) -> bool:
        def is_overlapping(contraction_1: Duration, contraction_2: Duration) -> bool:
            return (
                contraction_1.start_time < contraction_2.end_time
                and contraction_1.end_time > contraction_2.start_time
            )

        if len(labour.contractions) <= 1:
            return False

        pairs = itertools.combinations(labour.contractions, 2)
        return any(is_overlapping(c_1.duration, c_2.duration) for c_1, c_2 in pairs)
