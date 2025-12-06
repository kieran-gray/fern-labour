use std::fmt::Debug;

pub trait Aggregate: Sized + Debug + Clone {
    type Event: Clone + Debug;
    type Command: Debug;
    type Error: std::error::Error;

    fn aggregate_id(&self) -> String;

    fn apply(&mut self, event: &Self::Event);

    fn handle_command(
        state: Option<&Self>,
        command: Self::Command,
    ) -> Result<Vec<Self::Event>, Self::Error>;

    fn from_events(events: &[Self::Event]) -> Option<Self>;
}
