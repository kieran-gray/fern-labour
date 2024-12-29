from unittest.mock import Mock

from app.infrastructure.events.kafka_event_consumer import KafkaEventConsumer


def test_create_kafka_event_consumer():
    KafkaEventConsumer(["test"], "test", Mock())


async def test_consumer_closed_when_no_event_handlers_registered():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(["test"], "test", mock_consumer)
    consumer._handlers = None

    await consumer.start()
    assert consumer._running is False
    assert mock_consumer.close.called


async def test_consumer_has_assignments_is_healthy():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(["test"], "test", mock_consumer)

    mock_consumer.assignment = Mock(return_value=set("test"))
    assert await consumer.is_healthy()


async def test_consumer_has_no_assignments_is_unhealthy():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(["test"], "test", mock_consumer)

    assert not await consumer.is_healthy()


async def test_consumer_has_no_kafka_consumer_is_unhealthy():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(["test"], "test", mock_consumer)
    consumer._consumer = None

    assert not await consumer.is_healthy()
