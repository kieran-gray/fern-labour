from fern_labour_notifications_shared.enums import NotificationTemplate

TEMPLATE_TO_TWILIO_TEMPLATE_SID = {
    NotificationTemplate.LABOUR_ANNOUNCEMENT: "HX41e6683ac06893d80af526ed09c2171a",
    NotificationTemplate.LABOUR_BEGUN: "HX9e260e6602743e312b327ac866e8b39f",
    NotificationTemplate.LABOUR_COMPLETED: "HX759db0f512d2bdd1f2a2ed445a21fbf4",
    NotificationTemplate.LABOUR_COMPLETED_WITH_NOTE: "HXa4be7b7f652ad8efe00ef81223b85c6a",
}


TEMPLATE_TO_MESSAGE_CONTENT_VARIABLES = {
    NotificationTemplate.LABOUR_ANNOUNCEMENT: {
        "1": "subscriber_first_name",
        "2": "birthing_person_name",
        "3": "announcement",
    },
    NotificationTemplate.LABOUR_BEGUN: {
        "1": "subscriber_first_name",
        "2": "birthing_person_name",
        "3": "link",
    },
    NotificationTemplate.LABOUR_COMPLETED: {
        "1": "subscriber_first_name",
        "2": "birthing_person_name",
        "3": "link",
    },
    NotificationTemplate.LABOUR_COMPLETED_WITH_NOTE: {
        "1": "subscriber_first_name",
        "2": "birthing_person_name",
        "3": "update",
    },
}
