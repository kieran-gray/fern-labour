from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.contraction.entity import Contraction
from app.domain.contraction.events import ContractionEnded, ContractionStarted
from app.domain.labour.enums import LabourPhase
from app.domain.labour.events import (
    LabourBegun,
    LabourCompleted,
    LabourPlanned,
    LabourUpdatePosted,
)
from app.domain.labour.vo_labour_id import LabourId
from app.domain.labour_update.entity import LabourUpdate
from app.domain.labour_update.enums import LabourUpdateType
from app.domain.user.vo_user_id import UserId


@dataclass(eq=False, kw_only=True)
class Labour(AggregateRoot[LabourId]):
    """
    Aggregate root for tracking labour.
    Maintains consistency across all contractions and enforces labour-specific rules.
    """

    birthing_person_id: UserId
    current_phase: LabourPhase = LabourPhase.PLANNED
    first_labour: bool
    due_date: datetime
    contractions: list[Contraction] = field(default_factory=list)
    labour_updates: list[LabourUpdate] = field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None
    labour_name: str | None = None
    notes: str | None = None

    @classmethod
    def plan(
        cls,
        birthing_person_id: UserId,
        first_labour: bool,
        due_date: datetime,
        labour_name: str | None = None,
        labour_id: UUID | None = None,
    ) -> Self:
        labour = cls(
            id_=LabourId(labour_id or uuid4()),
            birthing_person_id=birthing_person_id,
            first_labour=first_labour,
            due_date=due_date,
            labour_name=labour_name,
        )
        labour.add_domain_event(
            LabourPlanned.create(
                data={
                    "labour_id": str(labour.id_.value),
                    "birthing_person_id": labour.birthing_person_id.value,
                }
            )
        )
        return labour

    def update_plan(
        self, first_labour: bool, due_date: datetime, labour_name: str | None = None
    ) -> None:
        self.first_labour = first_labour
        self.due_date = due_date
        self.labour_name = labour_name

    def begin(self, start_time: datetime | None = None) -> None:
        self.start_time = start_time or datetime.now(UTC)
        self.set_labour_phase(LabourPhase.EARLY)
        self.add_domain_event(
            LabourBegun.create(
                data={
                    "labour_id": str(self.id_.value),
                    "birthing_person_id": self.birthing_person_id.value,
                    "start_time": self.start_time.isoformat(),
                    "notes": self.notes if self.notes else "",
                }
            )
        )

    @property
    def is_active(self) -> bool:
        return self.end_time is None

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

    def start_contraction(
        self,
        intensity: int | None = None,
        start_time: datetime | None = None,
        notes: str | None = None,
    ) -> Contraction:
        """Start a new contraction in this session"""
        if self.current_phase is LabourPhase.PLANNED:
            self.begin(start_time=start_time)
        contraction = Contraction.start(
            labour_id=self.id_,
            start_time=start_time,
            intensity=intensity,
            notes=notes,
        )
        self.contractions.append(contraction)
        self.add_domain_event(ContractionStarted.from_contraction(contraction=contraction))
        return contraction

    def end_contraction(
        self,
        intensity: int,
        end_time: datetime | None = None,
        notes: str | None = None,
    ) -> None:
        """End the currently active contraction"""
        assert self.active_contraction
        active_contraction = self.active_contraction
        if notes:
            active_contraction.notes = notes
        active_contraction.end(end_time=end_time or datetime.now(UTC), intensity=intensity)
        self.add_domain_event(ContractionEnded.from_contraction(contraction=active_contraction))

    def set_labour_phase(self, labour_phase: LabourPhase) -> None:
        self.current_phase = labour_phase

    def complete_labour(self, end_time: datetime | None = None, notes: str | None = None) -> None:
        """Mark the labour as complete"""
        self.end_time = end_time or datetime.now(UTC)
        self.current_phase = LabourPhase.COMPLETE
        if notes:
            self.notes = notes
        self.add_domain_event(
            LabourCompleted.create(
                data={
                    "labour_id": str(self.id_.value),
                    "birthing_person_id": self.birthing_person_id.value,
                    "end_time": self.end_time.isoformat(),
                    "notes": self.notes if self.notes else "",
                }
            )
        )

    @property
    def announcements(self) -> list[LabourUpdate]:
        return [
            update
            for update in self.labour_updates
            if update.labour_update_type is LabourUpdateType.ANNOUNCEMENT
        ]

    @property
    def status_updates(self) -> list[LabourUpdate]:
        return [
            update
            for update in self.labour_updates
            if update.labour_update_type is LabourUpdateType.STATUS_UPDATE
        ]

    def add_labour_update(
        self, labour_update_type: LabourUpdateType, message: str, sent_time: datetime | None = None
    ) -> None:
        labour_update = LabourUpdate.create(
            labour_id=self.id_,
            labour_update_type=labour_update_type,
            message=message,
            sent_time=sent_time,
        )
        self.labour_updates.append(labour_update)
        self.add_domain_event(
            LabourUpdatePosted.create(
                {
                    "birthing_person_id": self.birthing_person_id.value,
                    "labour_id": str(self.id_.value),
                    "labour_update_type": labour_update_type.value,
                    "labour_update_id": str(labour_update.id_.value),
                    "message": labour_update.message,
                    "sent_time": labour_update.sent_time.isoformat(),
                }
            )
        )
