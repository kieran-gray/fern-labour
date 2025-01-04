from dataclasses import dataclass
from typing import Any

from app.domain.subscriber.enums import ContactMethod


@dataclass
class Notification:
    type: ContactMethod
    message: str
    destination: str
    subject: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "destination": self.destination,
            "subject": self.subject or "",
        }
