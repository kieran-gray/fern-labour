import logging

from app.labour.application.dtos.labour import LabourDTO
from app.labour.domain.labour.exceptions import UnauthorizedLabourRequest

log = logging.getLogger(__name__)


class LabourAuthorizationService:
    """
    Centralized service for handling authorization rules related to Labours.
    Methods raise specific Unauthorized exceptions if the check fails.
    """

    async def ensure_can_access_labour(self, requester_id: str, labour: LabourDTO) -> None:
        """
        Checks if the user can access the labour
        Rule: Requester is birthing person
        """
        if labour.birthing_person_id != requester_id:
            log.warning(f"User {requester_id} unauthorized to access labour {labour.id}")
            raise UnauthorizedLabourRequest()
