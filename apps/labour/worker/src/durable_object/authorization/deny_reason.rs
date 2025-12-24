use crate::durable_object::authorization::Capability;

#[derive(Debug, Clone, PartialEq)]
pub enum DenyReason {
    Unassociated,
    SubscriptionNotActive,
    CannotTargetOthers,
    MissingCapability(Capability),
}

impl std::fmt::Display for DenyReason {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DenyReason::Unassociated => write!(f, "Not associated with this labour"),
            DenyReason::SubscriptionNotActive => write!(f, "Subscription is not active"),
            DenyReason::CannotTargetOthers => {
                write!(f, "Can only manage your own subscription")
            }
            DenyReason::MissingCapability(cap) => {
                write!(f, "Missing required capability: {:?}", cap)
            }
        }
    }
}

impl std::error::Error for DenyReason {}
