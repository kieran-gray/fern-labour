from fern_labour_notifications_shared.enums import NotificationTemplate

TEMPLATE_TO_MESSAGE_STRING_TEMPLATE = {
    NotificationTemplate.LABOUR_ANNOUNCEMENT: (
        "Hey {subscriber_first_name},\n"
        "{birthing_person_first_name} has shared a new message with you through FernLabour:\n"
        "{announcement}"
    ),
    NotificationTemplate.LABOUR_BEGUN: (
        "Hey {subscriber_first_name},\n"
        "Exiting news, {birthing_person_first_name} has started labour!\n"
        "Remember that things can be slow at first, so please be patient and check FernLabour for "
        "any updates."
    ),
    NotificationTemplate.LABOUR_COMPLETED: (
        "Hey {subscriber_first_name},\n"
        "Wonderful news, {birthing_person_first_name} has completed labour!"
    ),
    NotificationTemplate.LABOUR_COMPLETED_WITH_NOTE: (
        "Hey {subscriber_first_name},\n"
        "Wonderful news, {birthing_person_first_name} has completed labour!\n"
        "They added the following note:\n"
        "{update}"
    ),
    NotificationTemplate.LABOUR_UPDATE: "Hey {subscriber_first_name}, {update}",
}
