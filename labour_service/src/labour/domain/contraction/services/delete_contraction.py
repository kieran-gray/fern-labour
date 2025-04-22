from src.labour.domain.contraction.exceptions import (
    CannotDeleteActiveContraction,
    ContractionNotFoundById,
)
from src.labour.domain.contraction.value_objects.contraction_id import ContractionId
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.exceptions import LabourAlreadyCompleted


class DeleteContractionService:
    def delete_contraction(self, labour: Labour, contraction_id: ContractionId) -> Labour:
        if labour.current_phase == LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()

        contraction = next(
            (
                contraction
                for contraction in labour.contractions
                if contraction.id_ == contraction_id
            ),
            None,
        )
        if not contraction:
            raise ContractionNotFoundById(contraction_id=contraction_id.value)

        if contraction.is_active:
            raise CannotDeleteActiveContraction()

        labour.contractions.remove(contraction)

        return labour
