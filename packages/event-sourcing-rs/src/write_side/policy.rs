pub struct PolicyContext<'a, A> {
    pub state: &'a A,
    pub sequence: i64,
}

impl<'a, A> PolicyContext<'a, A> {
    pub fn new(state: &'a A, sequence: i64) -> Self {
        Self { state, sequence }
    }
}

pub type PolicyFn<E, A, R> = fn(&E, &PolicyContext<'_, A>) -> Vec<R>;

pub trait HasPolicies<A: 'static, R: 'static>: Sized + 'static {
    fn policies() -> &'static [PolicyFn<Self, A, R>];

    fn apply_policies(&self, ctx: &PolicyContext<'_, A>) -> Vec<R> {
        Self::policies()
            .iter()
            .flat_map(|f| f(self, ctx))
            .collect()
    }
}
