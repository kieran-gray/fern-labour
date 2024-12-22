from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonHasActiveLabour
from app.domain.labour.entity import Labour


class BeginLabourService:
    def begin_labour(
        self, birthing_person: BirthingPerson, first_labour: bool | None = None
    ) -> BirthingPerson:
        if birthing_person.has_active_labour:
            raise BirthingPersonHasActiveLabour(birthing_person.id_)

        labour = Labour.begin(
            birthing_person_id=birthing_person.id_,
            first_labour=first_labour or birthing_person.first_labour,
        )

        birthing_person.add_labour(labour)

        return birthing_person
