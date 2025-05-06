from enum import StrEnum

from src.subscription.domain.enums import SubscriptionAccessLevel


class Product(StrEnum):
    UPGRADE_TO_SUPPORTER = "upgrade_to_supporter"


STRIPE_PRODUCT_TO_ACCESS_LEVEL: dict[str, str] = {
    Product.UPGRADE_TO_SUPPORTER.value: SubscriptionAccessLevel.SUPPORTER.value,
}
