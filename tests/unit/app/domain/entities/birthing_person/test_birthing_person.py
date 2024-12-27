from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId


def test_birthing_person_init():
    birthing_person_id = "12345678-1234-5678-1234-567812345678"
    first_name = "test"
    last_name = "test"

    vo_birthing_person_id = BirthingPersonId(birthing_person_id)

    direct_birthing_person = BirthingPerson(
        id_=vo_birthing_person_id,
        first_name=first_name,
        last_name=last_name,
        first_labour=False,
    )

    indirect_birthing_person = BirthingPerson.create(
        birthing_person_id=birthing_person_id,
        first_name=first_name,
        last_name=last_name,
        first_labour=False,
    )

    assert isinstance(indirect_birthing_person, BirthingPerson)
    assert direct_birthing_person.id_ == vo_birthing_person_id == indirect_birthing_person.id_
