from dataclasses import dataclass
from typing import Any


@dataclass
class LabourUpdateData:
    birthing_person_name: str
    subscriber_first_name: str
    update: str
    link: str
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "subscriber_first_name": self.subscriber_first_name,
            "update": self.update,
            "link": self.link,
            "notes": self.notes,
        }


@dataclass
class ContactUsData:
    email: str
    name: str
    message: str
    user_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "email": self.email,
            "name": self.name,
            "message": self.message,
            "user_id": self.user_id,
        }


@dataclass
class LabourInviteData:
    birthing_person_name: str
    birthing_person_first_name: str
    link: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "birthing_person_first_name": self.birthing_person_first_name,
            "link": self.link,
        }


@dataclass
class SubscriberInviteData:
    subscriber_name: str
    link: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "subscriber_name": self.subscriber_name,
            "link": self.link,
        }
