from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite, relationship

from app.common.infrastructure.persistence.orm_registry import mapper_registry
from app.labour.domain.contraction.entity import Contraction
from app.labour.domain.contraction.value_objects.contraction_duration import Duration
from app.labour.domain.contraction.value_objects.contraction_id import ContractionId
from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.labour_update.entity import LabourUpdate
from app.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId
from app.labour.infrastructure.persistence.tables.contractions import contractions_table
from app.labour.infrastructure.persistence.tables.labour_updates import labour_updates_table
from app.labour.infrastructure.persistence.tables.labours import labours_table
from app.user.domain.value_objects.user_id import UserId

mapper_registry.map_imperatively(
    LabourUpdate,
    labour_updates_table,
    properties={
        "id_": composite(LabourUpdateId, labour_updates_table.c.id),
        "labour_update_type": labour_updates_table.c.labour_update_type,
        "labour_id": composite(LabourId, labour_updates_table.c.labour_id),
        "message": labour_updates_table.c.message,
        "sent_time": labour_updates_table.c.sent_time,
    },
    column_prefix="_",
)

mapper_registry.map_imperatively(
    Contraction,
    contractions_table,
    properties={
        "id_": composite(ContractionId, contractions_table.c.id),
        "labour_id": composite(LabourId, contractions_table.c.labour_id),
        "duration": composite(
            Duration, contractions_table.c.start_time, contractions_table.c.end_time
        ),
        "intensity": contractions_table.c.intensity,
        "notes": contractions_table.c.notes,
    },
    column_prefix="_",
)


mapper_registry.map_imperatively(
    Labour,
    labours_table,
    properties={
        "id_": composite(LabourId, labours_table.c.id),
        "birthing_person_id": composite(UserId, labours_table.c.birthing_person_id),
        "current_phase": labours_table.c.current_phase,
        "first_labour": labours_table.c.first_labour,
        "due_date": labours_table.c.due_date,
        "labour_name": labours_table.c.labour_name,
        "payment_plan": labours_table.c.payment_plan,
        "contractions": relationship(
            Contraction,
            order_by=contractions_table.c.start_time,
            cascade="all, delete-orphan",
            lazy="selectin",
        ),
        "labour_updates": relationship(
            LabourUpdate,
            order_by=labour_updates_table.c.sent_time,
            cascade="all, delete-orphan",
            lazy="selectin",
        ),
        "start_time": labours_table.c.start_time,
        "end_time": labours_table.c.end_time,
        "notes": labours_table.c.notes,
    },
    column_prefix="_",
)


@event.listens_for(Labour, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
