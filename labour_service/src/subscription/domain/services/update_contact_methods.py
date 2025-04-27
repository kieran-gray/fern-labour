from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import ContactMethod


class UpdateContactMethodsService:
    def update_contact_methods(
        self, subscription: Subscription, contact_methods: list[ContactMethod]
    ) -> Subscription:
        # Filter out SMS if Whatsapp is also enabled. If Whatsapp sending fails Twilio will
        # auto fallback to SMS anyway.
        # Plus, people don't want a text and a Whatsapp.
        if ContactMethod.WHATSAPP in contact_methods and ContactMethod.SMS in contact_methods:
            contact_methods.remove(ContactMethod.SMS)

        subscription.update_contact_methods(contact_methods)

        return subscription
