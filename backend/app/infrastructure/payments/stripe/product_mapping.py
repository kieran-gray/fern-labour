from enum import StrEnum

from app.domain.labour.enums import LabourPaymentPlan


class Product(StrEnum):
    UPGRADE_TO_INNER_CIRCLE = "upgrade_to_inner_circle"
    UPGRADE_TO_COMMUNITY = "upgrade_to_community"
    UPGRADE_TO_COMMUNITY_FROM_INNER_CIRCLE = "upgrade_to_community_from_inner_circle"


STRIPE_PRODUCT_TO_PAYMENT_PLAN: dict[str, str] = {
    Product.UPGRADE_TO_INNER_CIRCLE.value: LabourPaymentPlan.INNER_CIRCLE.value,
    Product.UPGRADE_TO_COMMUNITY.value: LabourPaymentPlan.COMMUNITY.value,
    Product.UPGRADE_TO_COMMUNITY_FROM_INNER_CIRCLE.value: LabourPaymentPlan.COMMUNITY.value,
}
