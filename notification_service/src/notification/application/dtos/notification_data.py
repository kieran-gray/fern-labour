from dataclasses import dataclass
from typing import Any, Protocol, Self

from src.notification.domain.enums import NotificationTemplate


class BaseNotificationData(Protocol):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...

    def to_dict(self) -> dict[str, Any]: ...


@dataclass
class LabourUpdateData(BaseNotificationData):
    birthing_person_name: str
    subscriber_first_name: str
    update: str
    link: str
    notes: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            birthing_person_name=data["birthing_person_name"],
            subscriber_first_name=data["subscriber_first_name"],
            update=data["update"],
            link=data["link"],
            notes=data["notes"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "subscriber_first_name": self.subscriber_first_name,
            "update": self.update,
            "link": self.link,
            "notes": self.notes,
        }


@dataclass
class LabourAnnouncementData(BaseNotificationData):
    birthing_person_name: str
    birthing_person_first_name: str
    subscriber_first_name: str
    announcement: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            birthing_person_name=data["birthing_person_name"],
            birthing_person_first_name=data["birthing_person_first_name"],
            subscriber_first_name=data["subscriber_first_name"],
            announcement=data["announcement"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "birthing_person_first_name": self.birthing_person_first_name,
            "subscriber_first_name": self.subscriber_first_name,
            "announcement": self.announcement,
            "link": self.link,
        }


@dataclass
class LabourBegunData(BaseNotificationData):
    birthing_person_name: str
    birthing_person_first_name: str
    subscriber_first_name: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            birthing_person_name=data["birthing_person_name"],
            birthing_person_first_name=data["birthing_person_first_name"],
            subscriber_first_name=data["subscriber_first_name"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "birthing_person_first_name": self.birthing_person_first_name,
            "subscriber_first_name": self.subscriber_first_name,
            "link": self.link,
        }


@dataclass
class LabourCompletedWithNoteData(BaseNotificationData):
    birthing_person_name: str
    birthing_person_first_name: str
    subscriber_first_name: str
    update: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            birthing_person_name=data["birthing_person_name"],
            birthing_person_first_name=data["birthing_person_first_name"],
            subscriber_first_name=data["subscriber_first_name"],
            update=data["update"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "birthing_person_first_name": self.birthing_person_first_name,
            "subscriber_first_name": self.subscriber_first_name,
            "update": self.update,
            "link": self.link,
        }


@dataclass
class LabourCompletedData(BaseNotificationData):
    birthing_person_name: str
    birthing_person_first_name: str
    subscriber_first_name: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            birthing_person_name=data["birthing_person_name"],
            birthing_person_first_name=data["birthing_person_first_name"],
            subscriber_first_name=data["subscriber_first_name"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "birthing_person_first_name": self.birthing_person_first_name,
            "subscriber_first_name": self.subscriber_first_name,
            "link": self.link,
        }


@dataclass
class ContactUsData(BaseNotificationData):
    email: str
    name: str
    message: str
    user_id: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            email=data["email"],
            name=data["name"],
            message=data["message"],
            user_id=data["user_id"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "email": self.email,
            "name": self.name,
            "message": self.message,
            "user_id": self.user_id,
        }


@dataclass
class LabourInviteData(BaseNotificationData):
    birthing_person_name: str
    birthing_person_first_name: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            birthing_person_name=data["birthing_person_name"],
            birthing_person_first_name=data["birthing_person_first_name"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_name": self.birthing_person_name,
            "birthing_person_first_name": self.birthing_person_first_name,
            "link": self.link,
        }


@dataclass
class SubscriberInviteData(BaseNotificationData):
    subscriber_name: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            subscriber_name=data["subscriber_name"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subscriber_name": self.subscriber_name,
            "link": self.link,
        }


@dataclass
class SubscriberRequestedData(BaseNotificationData):
    birthing_person_first_name: str
    subscriber_name: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            birthing_person_first_name=data["birthing_person_first_name"],
            subscriber_name=data["subscriber_name"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "birthing_person_first_name": self.birthing_person_first_name,
            "subscriber_name": self.subscriber_name,
            "link": self.link,
        }


@dataclass
class SubscriberApprovedData(BaseNotificationData):
    subscriber_first_name: str
    birthing_person_name: str
    link: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            subscriber_first_name=data["subscriber_first_name"],
            birthing_person_name=data["birthing_person_name"],
            link=data["link"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subscriber_first_name": self.subscriber_first_name,
            "birthing_person_name": self.birthing_person_name,
            "link": self.link,
        }


TEMPLATE_TO_PAYLOAD: dict[NotificationTemplate, type[BaseNotificationData]] = {
    NotificationTemplate.LABOUR_ANNOUNCEMENT: LabourAnnouncementData,
    NotificationTemplate.LABOUR_BEGUN: LabourBegunData,
    NotificationTemplate.LABOUR_COMPLETED: LabourCompletedData,
    NotificationTemplate.LABOUR_COMPLETED_WITH_NOTE: LabourCompletedWithNoteData,
    NotificationTemplate.LABOUR_UPDATE: LabourUpdateData,
    NotificationTemplate.LABOUR_INVITE: LabourInviteData,
    NotificationTemplate.CONTACT_US_SUBMISSION: ContactUsData,
    NotificationTemplate.SUBSCRIBER_APPROVED: SubscriberApprovedData,
    NotificationTemplate.SUBSCRIBER_INVITE: SubscriberInviteData,
    NotificationTemplate.SUBSCRIBER_REQUESTED: SubscriberRequestedData,
}
