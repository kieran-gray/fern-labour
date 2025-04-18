from src.notification.domain.enums import NotificationTemplate

TEMPLATE_TO_SUBJECT_STRING_TEMPLATE = {
    NotificationTemplate.CONTACT_US_SUBMISSION: "Contact us submission from: {email}",
    NotificationTemplate.LABOUR_INVITE: "Special invitation: Follow our baby's arrival journey 👶",
    NotificationTemplate.SUBSCRIBER_INVITE: "A Brilliant Way to Share Your Baby Journey! 🍼",
    NotificationTemplate.LABOUR_UPDATE: "Labour update from {birthing_person_name}",
}
