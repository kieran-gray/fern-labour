from dishka import Provider, Scope, provide

from app.application.events.producer import EventProducer
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
)
from app.infrastructure.events.kafka_event_producer import KafkaEventProducer
from app.infrastructure.notifications.email.email_notification_gateway import (
    SFTPEmailNotificationGateway,
)
from app.infrastructure.notifications.sms.twilio_sms_notification_gateway import (
    TwilioSMSNotificationGateway,
)


class NotificationGatewayProvider(Provider):
    email_notification_gateway = provide(
        source=SFTPEmailNotificationGateway,
        scope=Scope.APP,
        provides=EmailNotificationGateway,
    )

    sms_notification_gateway = provide(
        source=TwilioSMSNotificationGateway,
        scope=Scope.APP,
        provides=SMSNotificationGateway,
    )


class EventProducerProvider(Provider):
    kafka_event_producer = provide(
        source=KafkaEventProducer,
        scope=Scope.APP,
        provides=EventProducer,
    )
