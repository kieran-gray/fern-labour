from enum import StrEnum


class LabourPhase(StrEnum):
    """Represents the different phases of labour"""

    PLANNED = "planned"
    EARLY = "early"
    ACTIVE = "active"
    TRANSITION = "transition"
    PUSHING = "pushing"
    COMPLETE = "complete"


class LabourPaymentPlan(StrEnum):
    """Represents the different plans available for a labour"""

    SOLO = "solo"
    INNER_CIRCLE = "inner_circle"
    COMMUNITY = "community"
