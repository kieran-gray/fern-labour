use anyhow::Result;

pub trait CommandHandler<C> {
    type Aggregate;
    type Event;

    fn handle(&self, command: C, aggregate: Option<&Self::Aggregate>) -> Result<Vec<Self::Event>>;

    fn load_aggregate(&self) -> Result<Option<Self::Aggregate>>;

    fn apply_events(
        &self,
        aggregate: Option<Self::Aggregate>,
        events: &[Self::Event],
    ) -> Option<Self::Aggregate>;
}
