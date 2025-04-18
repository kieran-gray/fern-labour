from src.common.application.enums import ResponseStatusEnum


def test_response_status_enum():
    assert ResponseStatusEnum.CREATED == ResponseStatusEnum("created")
    assert ResponseStatusEnum.UPDATED == ResponseStatusEnum("updated")
    assert ResponseStatusEnum.DELETED == ResponseStatusEnum("deleted")
