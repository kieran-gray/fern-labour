import json
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from app.application.dtos.labour_statistics import LabourStatisticsDTO
from app.domain.contraction.entity import Contraction
from app.domain.labour.vo_labour_id import LabourId


def get_start_time(last_start_time: datetime | None, start_time: datetime | None) -> datetime:
    if last_start_time:
        return last_start_time + timedelta(minutes=3)
    else:
        return start_time or datetime.now() - timedelta(hours=2)


def generate_contractions(count: int, start_time: datetime | None = None) -> dict[str, Any]:
    contraction_list = []
    last_start_time = None
    for _ in range(count):
        start_time = get_start_time(last_start_time, start_time)
        end_time = start_time + timedelta(minutes=1)

        contraction = Contraction.start(labour_id=LabourId(uuid4()), start_time=start_time)
        contraction.end(end_time=end_time, intensity=5)

        contraction_list.append(contraction)
        last_start_time = start_time

    return contraction_list


def test_can_create_labour_statistics_dto() -> None:
    dto = LabourStatisticsDTO.from_contractions(generate_contractions(40))
    assert dto.total
    assert dto.total.contraction_count == 40
    assert dto.last_30_mins
    assert dto.last_30_mins.contraction_count == 9
    assert dto.last_60_mins
    assert dto.last_60_mins.contraction_count == 19


def test_labour_statistics_dto_empty_less_than_3_contractions() -> None:
    dto = LabourStatisticsDTO.from_contractions(generate_contractions(2))
    assert not dto.total
    assert not dto.last_30_mins
    assert not dto.last_60_mins


def test_labour_statistics_dto_contractions_more_than_hour_ago() -> None:
    dto = LabourStatisticsDTO.from_contractions(generate_contractions(10, datetime(2020, 1, 1)))
    assert dto.total
    assert dto.total.contraction_count == 10
    assert not dto.last_30_mins
    assert not dto.last_60_mins


def test_can_convert_labour_statistics_dto_to_dict() -> None:
    dto = LabourStatisticsDTO.from_contractions(generate_contractions(10))
    labour_statistics_dict = dto.to_dict()
    json.dumps(labour_statistics_dict)
