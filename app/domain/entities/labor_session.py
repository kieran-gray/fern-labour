from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from app.domain.base.entity import Entity
from app.domain.constants.labor_session import (
    CONTRACTIONS_REQUIRED_NULLIPAROUS,
    CONTRACTIONS_REQUIRED_PAROUS,
    LENGTH_OF_CONTRACTIONS_MINUTES,
    TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    TIME_BETWEEN_CONTRACTIONS_PAROUS,
)
from app.domain.entities.contraction import Contraction
from app.domain.exceptions.labor_session import (
    CannotCompleteLaborSessionWithActiveContraction,
    LaborSessionCompleted,
    LaborSessionHasActiveContraction,
    LaborSessionHasNoActiveContraction,
)
from app.domain.value_objects.labor_session_id import LaborSessionId


class LaborPhase(StrEnum):
    """Represents the different phases of labor"""

    EARLY = "early"
    ACTIVE = "active"
    TRANSITION = "transition"
    PUSHING = "pushing"
    COMPLETE = "complete"


@dataclass(eq=False, kw_only=True)
class LaborSession(Entity[LaborSessionId]):
    """
    Aggregate root for tracking a labor session.
    Maintains consistency across all contractions and enforces labor-specific rules.
    """

    user_id: UUID
    start_time: datetime
    first_labor: bool
    contractions: list[Contraction] = field(default_factory=list)
    current_phase: LaborPhase = LaborPhase.EARLY
    end_time: datetime | None = None
    notes: str | None = None

    @classmethod
    def start(
        cls,
        user_id: UUID,
        first_labor: bool,
        session_id: UUID | None = None,
        start_time: datetime | None = None,
    ) -> Self:
        """Start a new labor session"""
        return cls(
            id_=LaborSessionId(session_id or uuid4()),
            user_id=user_id,
            start_time=start_time or datetime.now(),
            first_labor=first_labor,
            contractions=[],
        )

    def start_contraction(
        self,
        intensity: int,
        start_time: datetime | None = None,
        notes: str | None = None,
    ) -> Contraction:
        """Start a new contraction in this session"""
        if self.has_active_contraction:
            raise LaborSessionHasActiveContraction()

        if self.current_phase == LaborPhase.COMPLETE:
            raise LaborSessionCompleted()

        contraction = Contraction.start(
            labor_session_id=self.id_.value,
            start_time=start_time,
            intensity=intensity,
            notes=notes,
        )
        self.contractions.append(contraction)
        return contraction

    def end_contraction(self, end_time: datetime | None = None) -> None:
        """End the currently active contraction"""
        if not self.has_active_contraction:
            raise LaborSessionHasNoActiveContraction()

        end_time = end_time or datetime.now()
        self.active_contraction.end(end_time)
        self._update_labor_phase()

    @property
    def active_contraction(self) -> Contraction | None:
        """Get the currently active contraction, if any"""
        return next(
            (contraction for contraction in self.contractions if contraction.is_active),
            None,
        )

    @property
    def has_active_contraction(self) -> bool:
        """Check if there's currently an active contraction"""
        return any(contraction.is_active for contraction in self.contractions)

    @property
    def should_go_to_hospital(self) -> bool:
        """
        When to go to the hospital depends on if this is a first labor or not.
        For a first time mum we should wait until contractions are well
        established. This means using the 3-1-1 rule:
        Contractions every 3 minutes, lasting 1 minute each, for 1 hour

        Otherwise we don't want to wait as long and should go to the hospital
        when contractions are once every 5 minutes for 30 minutes.
        """
        required_number_of_contractions = (
            CONTRACTIONS_REQUIRED_NULLIPAROUS if self.first_labor else CONTRACTIONS_REQUIRED_PAROUS
        )
        required_time_between_contractions = (
            TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS
            if self.first_labor
            else TIME_BETWEEN_CONTRACTIONS_PAROUS
        )

        if len(self.contractions) < required_number_of_contractions:
            return False

        recent_contractions = self.contractions[-required_number_of_contractions:]

        # Check if contractions are consistently 5 minutes apart or less
        for prev, curr in zip(recent_contractions, recent_contractions[1:], strict=False):
            time_between = (curr.start_time - prev.end_time).total_seconds() / 60
            if time_between > required_time_between_contractions:
                return False

        # Check if contractions are lasting about 1 minute
        if not all(
            c.duration.duration_minutes >= LENGTH_OF_CONTRACTIONS_MINUTES
            for c in recent_contractions
        ):
            return False

        # TODO this won't work if the contractions are hapening at a faster rate
        pattern_duration = recent_contractions[-1].end_time - recent_contractions[0].start_time
        return pattern_duration >= timedelta(hours=1)

    def _update_labor_phase(self) -> None:
        """
        Update the labor phase based on contraction patterns.
        This is a simplified version - in reality, this would likely involve
        additional medical data like dilation measurements.
        """
        if not self.contractions:
            return

        recent_contractions = self.contractions[-5:]  # Look at last 5 contractions
        avg_intensity = sum(c.intensity for c in recent_contractions) / len(recent_contractions)
        avg_duration = sum(c.duration.duration_minutes for c in recent_contractions) / len(
            recent_contractions
        )

        # Simplified phase determination logic
        if avg_intensity >= 8 and avg_duration >= 1.5:
            self.current_phase = LaborPhase.TRANSITION
        elif avg_intensity >= 6 and avg_duration >= 1:
            self.current_phase = LaborPhase.ACTIVE

    def complete_labor(self, end_time: datetime | None = None, notes: str | None = None) -> None:
        """Mark the labor session as complete"""
        if self.has_active_contraction:
            raise CannotCompleteLaborSessionWithActiveContraction()

        self.end_time = end_time or datetime.now()
        self.current_phase = LaborPhase.COMPLETE
        if notes:
            self.notes = notes

    def get_contraction_pattern(self) -> dict:
        """Analyze the current contraction pattern"""
        if len(self.contractions) < 3:
            return {"pattern": "Insufficient data"}

        recent = self.contractions[-3:]

        avg_duration = sum(c.duration.duration_minutes for c in recent) / len(recent)
        avg_intensity = sum(c.intensity for c in recent) / len(recent)

        # Calculate average time between contractions
        intervals = []
        for prev, curr in zip(recent, recent[1:], strict=False):
            interval = (curr.start_time - prev.end_time).total_seconds() / 60
            intervals.append(interval)
        avg_interval = sum(intervals) / len(intervals)

        return {
            "average_duration_minutes": round(avg_duration, 1),
            "average_intensity": round(avg_intensity, 1),
            "average_interval_minutes": round(avg_interval, 1),
            "phase": self.current_phase.value,
            "hospital_recommended": self.should_go_to_hospital,
        }
