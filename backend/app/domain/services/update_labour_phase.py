from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import LabourAlreadyCompleted


class UpdateLabourPhaseService:
    labour_phase_order = [
        LabourPhase.PLANNED,
        LabourPhase.EARLY,
        LabourPhase.ACTIVE,
        LabourPhase.TRANSITION,
        LabourPhase.PUSHING,
        LabourPhase.COMPLETE,
    ]

    def update_labour_phase(self, labour: Labour) -> Labour:
        if labour.current_phase is LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()

        recent_contractions = labour.contractions[-5:]
        avg_intensity = sum(c.intensity for c in recent_contractions if c.intensity) / len(
            recent_contractions
        )
        avg_duration = sum(c.duration.duration_minutes for c in recent_contractions) / len(
            recent_contractions
        )

        new_phase = labour.current_phase

        if avg_intensity >= 8 and avg_duration >= 1.5:
            new_phase = LabourPhase.TRANSITION
        elif avg_intensity >= 6 and avg_duration >= 1:
            new_phase = LabourPhase.ACTIVE

        if self.labour_phase_order.index(new_phase) > self.labour_phase_order.index(
            labour.current_phase
        ):
            labour.set_labour_phase(new_phase)

        return labour
