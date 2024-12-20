from sqlalchemy.orm import composite, relationship

from app.domain.contraction.entity import Contraction
from app.domain.contraction.vo_contraction_duration import Duration
from app.domain.contraction.vo_contraction_id import ContractionId
from app.domain.labour.entity import Labour
from app.domain.labour.vo_labor_session_id import LabourId
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.contractions import contractions_table
from app.infrastructure.persistence.tables.labor_sessions import labor_sessions_table

mapper_registry.map_imperatively(
    Contraction,
    contractions_table,
    properties={
        "id_": composite(ContractionId, contractions_table.c.id),
        "duration": composite(
            Duration, contractions_table.c.start_time, contractions_table.c.end_time
        ),
    },
    column_prefix="_",
)

mapper_registry.map_imperatively(
    Labour,
    labor_sessions_table,
    properties={
        "id_": composite(LabourId, labor_sessions_table.c.id),
        "contractions": relationship(
            Contraction,
            order_by=contractions_table.c.start_time,
            cascade="all, delete-orphan",
        ),
    },
    column_prefix="_",
)
