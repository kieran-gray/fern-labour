from dataclasses import dataclass

import pytest

from src.common.domain.aggregate_root import AggregateRoot
from src.common.domain.entity import Entity
from src.common.domain.value_object import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class SingleFieldValueObject(ValueObject):
    value: int


@dataclass(frozen=True, slots=True, repr=False)
class OtherSingleFieldValueObject(ValueObject):
    value: bool


@dataclass(frozen=True, slots=True, repr=False)
class MultiFieldValueObject(ValueObject):
    value1: int
    value2: str


@dataclass(eq=False, slots=True)
class SampleEntity(Entity[SingleFieldValueObject]):
    name: str


@dataclass(eq=False, slots=True)
class SampleAggregateRoot(AggregateRoot[SingleFieldValueObject]):
    name: str


@pytest.fixture
def single_field_value_object() -> SingleFieldValueObject:
    return SingleFieldValueObject(value=123)


@pytest.fixture
def other_single_field_value_object() -> OtherSingleFieldValueObject:
    return OtherSingleFieldValueObject(value=True)


@pytest.fixture
def multi_field_value_object() -> MultiFieldValueObject:
    return MultiFieldValueObject(value1=123, value2="abc")


@pytest.fixture
def sample_entity(
    single_field_value_object: SingleFieldValueObject,
) -> SampleEntity:
    return SampleEntity(id_=single_field_value_object, name="def")


@pytest.fixture
def sample_aggregate_root(single_field_value_object: SingleFieldValueObject):
    return SampleAggregateRoot(id_=single_field_value_object, name="def")
