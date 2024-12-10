from sqlalchemy.orm import composite, relationship

from app.domain.entities.contraction import Contraction
from app.domain.entities.labor_session import LaborSession
from app.domain.value_objects.contraction_duration import Duration
from app.domain.value_objects.contraction_id import ContractionId
from app.domain.value_objects.labor_session_id import LaborSessionId
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.contractions import contractions_table
from app.infrastructure.persistence.tables.labor_sessions import labor_sessions_table
from app.infrastructure.persistence.orm_registry import mapper_registry


mapper_registry.map_imperatively(
    Contraction,
    contractions_table,
    properties={
        "id_": composite(ContractionId, contractions_table.c.id),
        "duration": composite(
            Duration, contractions_table.c.start_time, contractions_table.c.end_time
        )
    },
    column_prefix="_",
)

mapper_registry.map_imperatively(
    LaborSession,
    labor_sessions_table,
    properties={
        "id_": composite(LaborSessionId, labor_sessions_table.c.id),
        "contractions": relationship(
            Contraction,
            order_by=contractions_table.c.start_time,
            cascade="all, delete-orphan",
        )
    },
    column_prefix="_",
)
