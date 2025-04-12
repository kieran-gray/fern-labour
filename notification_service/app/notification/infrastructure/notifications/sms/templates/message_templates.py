from app.notification.domain.enums import NotificationTemplate

TEMPLATE_TO_MESSAGE_STRING_TEMPLATE = {
    NotificationTemplate.LABOUR_UPDATE: "Hey {subscriber_first_name}, {update}",
}
