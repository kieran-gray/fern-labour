from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite, relationship

from app.domain.announcement.entity import Announcement
from app.domain.announcement.vo_announcement_id import AnnouncementId
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.contraction.entity import Contraction
from app.domain.contraction.vo_contraction_duration import Duration
from app.domain.contraction.vo_contraction_id import ContractionId
from app.domain.labour.entity import Labour
from app.domain.labour.vo_labour_id import LabourId
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.announcements import announcements_table
from app.infrastructure.persistence.tables.contractions import contractions_table
from app.infrastructure.persistence.tables.labours import labours_table

mapper_registry.map_imperatively(
    Announcement,
    announcements_table,
    properties={
        "id_": composite(AnnouncementId, announcements_table.c.id),
        "labour_id": composite(LabourId, announcements_table.c.labour_id),
        "message": announcements_table.c.message,
        "sent_time": announcements_table.c.sent_time,
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
        "birthing_person_id": composite(BirthingPersonId, labours_table.c.birthing_person_id),
        "start_time": labours_table.c.start_time,
        "first_labour": labours_table.c.first_labour,
        "contractions": relationship(
            Contraction,
            order_by=contractions_table.c.start_time,
            cascade="all, delete-orphan",
            lazy="selectin",
        ),
        "announcements": relationship(
            Announcement,
            order_by=announcements_table.c.sent_time,
            cascade="all, delete-orphan",
            lazy="selectin",
        ),
        "current_phase": labours_table.c.current_phase,
        "end_time": labours_table.c.end_time,
        "notes": labours_table.c.notes,
    },
    column_prefix="_",
)


@event.listens_for(Labour, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
