from src.user.application.dtos.user_summary import UserSummaryDTO


def test_can_serialize_user_summary_dto():
    data_dict = {
        "id": "test",
        "first_name": "name",
        "last_name": "LastName",
    }
    dto = UserSummaryDTO(**data_dict)
    assert dto.to_dict() == data_dict
