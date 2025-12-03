use std::any::Any;

pub trait EventReactor<E> {
    type OutputCommand;

    fn react(&self, events: &[E], aggregate_state: Option<&impl Any>) -> Vec<Self::OutputCommand>;
}
