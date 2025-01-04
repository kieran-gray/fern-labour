import logging
from datetime import UTC, datetime
from unittest.mock import Mock

import pytest  # noqa

from app.domain.base.event import DomainEvent
from app.infrastructure.events.kafka_event_producer import KafkaEventProducer


def test_create_kafka_event_producer():
    KafkaEventProducer(["test"], "all", 1, "prefix", Mock())


def test_kafka_event_producer_closed_on_del():
    mock_producer = Mock()
    producer = KafkaEventProducer(["test"], "all", 1, "prefix", mock_producer)

    del producer
    assert mock_producer.close.called


def test_kafka_event_producer_get_topic():
    mock_producer = Mock()
    producer = KafkaEventProducer(["test"], "all", 1, "prefix", mock_producer)

    event = DomainEvent("test", "test-event", {"data": 123}, datetime.now(UTC))
    assert producer._get_topic(event) == "prefix.test-event"


def test_kafka_event_producer_get_topic_fixes_case():
    mock_producer = Mock()
    producer = KafkaEventProducer(["test"], "all", 1, "prefix", mock_producer)

    event = DomainEvent("test", "TEST-EVENT", {"data": 123}, datetime.now(UTC))
    assert producer._get_topic(event) == "prefix.test-event"


async def test_kafka_event_producer_publish_event():
    mock_producer = Mock()
    producer = KafkaEventProducer(["test"], "all", 1, "prefix", mock_producer)

    event = DomainEvent("test", "test-event", {"data": 123}, datetime.now(UTC))
    await producer.publish(event)

    assert mock_producer.send.call_count == 1
    assert mock_producer.flush.call_count == 1


async def test_kafka_event_producer_publish_event_failure_raises_log(caplog):
    mock_producer = Mock()
    producer = KafkaEventProducer(["test"], "all", 1, "prefix", mock_producer)

    event = DomainEvent("test", "test-event", {"data": 123}, datetime.now(UTC))
    mock_producer.send = Mock(side_effect=Exception)

    module = "app.infrastructure.events.kafka_event_producer"
    with caplog.at_level(logging.CRITICAL, logger=module):
        await producer.publish(event)
        assert len(caplog.records) == 1


async def test_kafka_event_producer_publish_event_batch():
    mock_producer = Mock()
    producer = KafkaEventProducer(["test"], "all", 1, "prefix", mock_producer)

    events = [DomainEvent("test", "test-event", {"data": 123}, datetime.now(UTC)) for i in range(5)]
    await producer.publish_batch(events)

    assert mock_producer.send.call_count == 5
    assert mock_producer.flush.call_count == 1


async def test_kafka_event_producer_publish_event_batch_failure_raises_logs(caplog):
    mock_producer = Mock()
    producer = KafkaEventProducer(["test"], "all", 1, "prefix", mock_producer)

    events = [DomainEvent("test", "test-event", {"data": 123}, datetime.now(UTC)) for i in range(5)]
    mock_producer.send = Mock(side_effect=Exception)

    module = "app.infrastructure.events.kafka_event_producer"
    with caplog.at_level(logging.CRITICAL, logger=module):
        await producer.publish_batch(events)
        assert len(caplog.records) == 1
