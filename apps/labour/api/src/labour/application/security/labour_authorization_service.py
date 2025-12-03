import logging
from uuid import UUID

from src.labour.domain.labour.exceptions import InvalidLabourId, UnauthorizedLabourRequest
from src.labour.domain.labour.repository import LabourRepository
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class LabourAuthorizationService:
    """
    Centralized service for handling authorization rules related to Labours.
    Methods raise specific Unauthorized exceptions if the check fails.
    """

    def __init__(self, labour_repository: LabourRepository):
        self._labour_repository = labour_repository

    async def ensure_can_access_labour(self, requester_id: str, labour_id: str) -> None:
        """
        Checks if the user can access the labour
        Rule: Requester is birthing person
        """
        requester_domain_id = UserId(requester_id)

        try:
            labour_domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

        labour_birthing_person_id = await self._labour_repository.get_birthing_person_id_for_labour(
            labour_id=labour_domain_id
        )

        if labour_birthing_person_id != requester_domain_id:
            log.warning(f"User {requester_id} unauthorized to access labour {labour_id}")
            raise UnauthorizedLabourRequest()
