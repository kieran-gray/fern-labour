from enum import StrEnum


class ContactMethod(StrEnum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"


class SubscriberRole(StrEnum):
    BIRTH_PARTNER = "birth_partner"
    FRIENDS_AND_FAMILY = "friends_and_family"


class SubscriptionStatus(StrEnum):
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBED = "unsubscribed"
    REQUESTED = "requested"
    REMOVED = "removed"
    BLOCKED = "blocked"


class SubscriptionAccessLevel(StrEnum):
    BASIC = "basic"
    SUPPORTER = "supporter"
