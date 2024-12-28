from datetime import datetime

import pytest

from app.domain.base.event import DomainEvent
from app.domain.base.exceptions import DomainError
from tests.unit.app.domain.base.conftest import SampleAggregateRoot, SingleFieldValueObject


def test_aggregate_root_id_invariance(sample_aggregate_root: SampleAggregateRoot) -> None:
    with pytest.raises(DomainError):
        sample_aggregate_root.id_ = SingleFieldValueObject(value=123)


def test_aggregate_root_has_domain_events(sample_aggregate_root: SampleAggregateRoot) -> None:
    assert hasattr(sample_aggregate_root, "_domain_events")
    assert sample_aggregate_root._domain_events == []


def test_aggregate_root_add_domain_event(sample_aggregate_root: SampleAggregateRoot) -> None:
    assert sample_aggregate_root._domain_events == []
    domain_event = DomainEvent("test", "test", {}, datetime.now())
    sample_aggregate_root.add_domain_event(domain_event)
    assert sample_aggregate_root.domain_events == [domain_event]


def test_aggregate_root_clear_domain_events(sample_aggregate_root: SampleAggregateRoot) -> None:
    domain_event = DomainEvent("test", "test", {}, datetime.now())
    sample_aggregate_root.add_domain_event(domain_event)
    assert sample_aggregate_root.domain_events == [domain_event]

    assert sample_aggregate_root.clear_domain_events() == [domain_event]
    assert sample_aggregate_root.domain_events == []
