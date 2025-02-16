from enum import StrEnum


class LabourUpdateType(StrEnum):
    """Represents the different types of labour update"""

    ANNOUNCEMENT = "announcement"
    STATUS_UPDATE = "status_update"
