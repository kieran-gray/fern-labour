from enum import StrEnum

from app.domain.labour.enums import LabourPaymentPlan


class Product(StrEnum):
    UPGRADE_TO_INNER_CIRCLE = "upgrade_to_inner_circle"
    UPGRADE_TO_COMMUNITY = "upgrade_to_community"
    UPGRADE_TO_COMMUNITY_FROM_INNER_CIRCLE = "upgrade_to_community_from_inner_circle"


STRIPE_PRICE_TO_PAYMENT_PLAN: dict[str, str] = {
    "price_1R0nsPJgYMUrJ4V8CoWZnONg": LabourPaymentPlan.INNER_CIRCLE.value,
    "price_1R1qYIJgYMUrJ4V8UpP8WBKO": LabourPaymentPlan.COMMUNITY.value,
    "price_1R1qYtJgYMUrJ4V8J20avp24": LabourPaymentPlan.COMMUNITY.value,
}


STRIPE_PRODUCT_TO_PRICE: dict[str, str] = {
    Product.UPGRADE_TO_INNER_CIRCLE.value: "price_1R0nsPJgYMUrJ4V8CoWZnONg",
    Product.UPGRADE_TO_COMMUNITY.value: "price_1R1qYIJgYMUrJ4V8UpP8WBKO",
    Product.UPGRADE_TO_COMMUNITY_FROM_INNER_CIRCLE.value: "price_1R1qYtJgYMUrJ4V8J20avp24",
}
