from dishka import Provider, Scope, provide

from app.application.interfaces.notfication_gateway import NotificationGateway
from app.infrastructure.notifications.email_notification_gateway import EmailNotificationGateway


class NotificationGatewayProvider(Provider):
    labour_repository = provide(
        source=EmailNotificationGateway,
        scope=Scope.REQUEST,
        provides=NotificationGateway,
    )
