from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase


class UpdateLabourPhaseService:
    labour_phase_order = [
        LabourPhase.EARLY,
        LabourPhase.ACTIVE,
        LabourPhase.TRANSITION,
        LabourPhase.PUSHING,
        LabourPhase.COMPLETE,
    ]

    def update_labour_phase(self, birthing_person: BirthingPerson) -> Labour:
        active_labour = birthing_person.active_labour

        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person.id_)

        assert birthing_person.active_labour
        recent_contractions = birthing_person.active_labour.contractions[-5:]
        avg_intensity = sum(c.intensity for c in recent_contractions if c.intensity) / len(
            recent_contractions
        )
        avg_duration = sum(c.duration.duration_minutes for c in recent_contractions) / len(
            recent_contractions
        )

        new_phase = active_labour.current_phase

        if avg_intensity >= 8 and avg_duration >= 1.5:
            new_phase = LabourPhase.TRANSITION
        elif avg_intensity >= 6 and avg_duration >= 1:
            new_phase = LabourPhase.ACTIVE

        if self.labour_phase_order.index(new_phase) > self.labour_phase_order.index(
            active_labour.current_phase
        ):
            active_labour.set_labour_phase(new_phase)

        return active_labour
