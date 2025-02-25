from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import LabourAlreadyBegun


class BeginLabourService:
    def begin_labour(self, labour: Labour) -> Labour:
        if labour.current_phase is not LabourPhase.PLANNED:
            raise LabourAlreadyBegun()

        labour.begin()

        return labour
