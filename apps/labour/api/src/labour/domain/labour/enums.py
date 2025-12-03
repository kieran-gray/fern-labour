from enum import StrEnum


class LabourPhase(StrEnum):
    """Represents the different phases of labour"""

    PLANNED = "planned"
    EARLY = "early"
    ACTIVE = "active"
    TRANSITION = "transition"
    PUSHING = "pushing"
    COMPLETE = "complete"
