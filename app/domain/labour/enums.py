from enum import StrEnum


class LabourPhase(StrEnum):
    """Represents the different phases of labor"""

    EARLY = "early"
    ACTIVE = "active"
    TRANSITION = "transition"
    PUSHING = "pushing"
    COMPLETE = "complete"
