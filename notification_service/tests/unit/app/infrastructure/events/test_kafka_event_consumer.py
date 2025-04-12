import logging
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from dishka import AsyncContainer
from kafka import KafkaConsumer

from app.common.application.event_handler import EventHandler
from app.common.infrastructure.events.kafka.kafka_event_consumer import (
    HandlerInfo,
    KafkaEventConsumer,
)
from app.setup.ioc.di_component_enum import ComponentEnum

MODULE = "app.infrastructure.events.kafka_event_consumer"


@pytest.fixture
def kafka_consumer_mock():
    return MagicMock(spec=KafkaConsumer)


@pytest.fixture
def async_container_mock():
    container = AsyncMock()
    container.scope.return_value = container
    return container


@pytest.fixture
def event_handler_mock():
    handler = AsyncMock(spec=EventHandler)
    handler.handle = AsyncMock()
    return handler


@pytest.fixture
def kafka_event_consumer(kafka_consumer_mock):
    return KafkaEventConsumer(
        bootstrap_servers="localhost:9092",
        group_id="test-group",
        topic_prefix="test-prefix",
        consumer=kafka_consumer_mock,
    )


async def test_set_container(
    kafka_event_consumer: KafkaEventConsumer, async_container_mock: AsyncContainer
):
    """Test setting the async container."""
    kafka_event_consumer.set_container(async_container_mock)
    assert kafka_event_consumer._container == async_container_mock


async def test_subscribe_to_topics(
    kafka_event_consumer: KafkaEventConsumer, kafka_consumer_mock: KafkaConsumer
):
    """Test that the consumer subscribes to the correct topics."""
    expected_topics = ["test-prefix.topic1", "test-prefix.topic2"]
    kafka_event_consumer._handlers = {topic: MagicMock() for topic in expected_topics}

    kafka_event_consumer._subscribe_to_topics()
    kafka_consumer_mock.subscribe.assert_called_with(topics=expected_topics)


async def test_subscribe_to_no_topics(caplog, kafka_event_consumer: KafkaEventConsumer):
    """Test that the consumer subscribes to the correct topics."""
    kafka_event_consumer._handlers = {}

    with caplog.at_level(logging.WARNING, logger=MODULE):
        kafka_event_consumer._subscribe_to_topics()
        assert len(caplog.records) == 1
        assert caplog.messages[0] == "No topics to subscribe to."


async def test_process_message_success(
    kafka_event_consumer: KafkaEventConsumer,
    async_container_mock: AsyncContainer,
    event_handler_mock: EventHandler,
):
    """Test successful processing of a single message."""
    message = MagicMock(topic="test-prefix.topic", value={"key": "value"})
    kafka_event_consumer._handlers = {
        "test-prefix.topic": HandlerInfo(
            type(event_handler_mock), ComponentEnum.NOTIFICATION_EVENTS
        )
    }
    async_container_mock.get.return_value = event_handler_mock

    await kafka_event_consumer._process_message(message, async_container_mock)

    async_container_mock.get.assert_called_once_with(
        type(event_handler_mock), component=ComponentEnum.NOTIFICATION_EVENTS
    )
    event_handler_mock.handle.assert_called_once_with({"key": "value"})


async def test_process_message_no_handler(
    caplog, kafka_event_consumer: KafkaEventConsumer, async_container_mock: AsyncContainer
):
    """Test processing a message with no registered handler."""
    message = MagicMock(topic="unknown-topic", value={"key": "value"})
    kafka_event_consumer._handlers = {}

    with caplog.at_level(logging.ERROR, logger=MODULE):
        await kafka_event_consumer._process_message(message, async_container_mock)
        assert len(caplog.records) == 1
        assert caplog.messages[0] == "No handler found for topic: unknown-topic"


async def test_process_message_handler_error(
    caplog,
    kafka_event_consumer: KafkaEventConsumer,
    async_container_mock: AsyncContainer,
    event_handler_mock: EventHandler,
):
    """Test processing a message where the handler raises an exception."""
    message = MagicMock(topic="test-prefix.topic", value={"key": "value"})
    kafka_event_consumer._handlers = {"test-prefix.topic": type(event_handler_mock)}
    async_container_mock.get.return_value = event_handler_mock
    event_handler_mock.handle.side_effect = Exception("Handler error")

    with caplog.at_level(logging.ERROR, logger=MODULE):
        await kafka_event_consumer._process_message(message, async_container_mock)
        assert len(caplog.records) == 1
        assert caplog.messages[0] == "Error processing message from topic test-prefix.topic."


async def test_start_stops_on_no_handlers(caplog, kafka_event_consumer: KafkaConsumer):
    """Test that the consumer stops if no handlers are registered."""
    kafka_event_consumer._handlers = {}
    kafka_event_consumer._running = True

    with patch.object(kafka_event_consumer, "stop", new_callable=AsyncMock) as mock_stop:
        with caplog.at_level(logging.ERROR, logger=MODULE):
            await kafka_event_consumer.start()
        mock_stop.assert_called_once()
        assert len(caplog.records) == 1
        assert caplog.messages[0] == "No event handlers registered."


async def test_stop(kafka_event_consumer: KafkaEventConsumer, kafka_consumer_mock: KafkaConsumer):
    """Test that the consumer stops."""
    kafka_event_consumer._running = True
    await kafka_event_consumer.stop()

    assert kafka_event_consumer._running is False
    kafka_consumer_mock.close.assert_called_once()


async def test_is_healthy(
    kafka_event_consumer: KafkaEventConsumer, kafka_consumer_mock: KafkaConsumer
):
    """Test health check of the Kafka consumer."""
    kafka_consumer_mock.assignment.return_value = ["partition1", "partition2"]
    assert await kafka_event_consumer.is_healthy() is True

    kafka_consumer_mock.assignment.side_effect = Exception("Error")
    assert await kafka_event_consumer.is_healthy() is False


async def test_handle_messages(caplog, kafka_event_consumer: KafkaEventConsumer):
    """Test handle without container set."""

    with caplog.at_level(logging.ERROR, logger=MODULE):
        await kafka_event_consumer._handle_messages({})
        assert len(caplog.records) == 1
        assert (
            caplog.messages[0] == "Dependency injection container not set. Cannot process messages."
        )


async def test_event_handler_mapping_has_prefix():
    prefix = "test_prefix"
    consumer = KafkaEventConsumer(
        bootstrap_servers=["test"], group_id="test", topic_prefix=prefix, consumer=Mock()
    )
    for event_handler in consumer._handlers.keys():
        assert event_handler.startswith("test_prefix.")


async def test_consumer_closed_when_no_event_handlers_registered():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(
        bootstrap_servers=["test"], group_id="test", topic_prefix="test", consumer=mock_consumer
    )
    consumer._handlers = None

    await consumer.start()
    assert consumer._running is False
    assert mock_consumer.close.called


async def test_consumer_has_assignments_is_healthy():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(
        bootstrap_servers=["test"], group_id="test", topic_prefix="test", consumer=mock_consumer
    )

    mock_consumer.assignment = Mock(return_value=set("test"))
    assert await consumer.is_healthy()


async def test_consumer_has_no_assignments_is_unhealthy():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(
        bootstrap_servers=["test"], group_id="test", topic_prefix="test", consumer=mock_consumer
    )

    assert not await consumer.is_healthy()


async def test_consumer_has_no_kafka_consumer_is_unhealthy():
    mock_consumer = Mock()
    consumer = KafkaEventConsumer(
        bootstrap_servers=["test"], group_id="test", topic_prefix="test", consumer=mock_consumer
    )
    consumer._consumer = None

    assert not await consumer.is_healthy()
