from src.labour.infrastructure.persistence.mappings.labour import (
    map_contractions_table,
    map_labour_updates_table,
    map_labours_table,
)
from src.subscription.infrastructure.persistence.mappings.subscription import (
    map_subscriptions_table,
)


def map_all() -> None:
    map_labour_updates_table()
    map_contractions_table()
    map_labours_table()
    map_subscriptions_table()
