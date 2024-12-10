from app.domain.exceptions.contraction import ContractionOverlaps
from app.domain.value_objects.contraction_duration import Duration


class ContractionService:
    def calculate_time_between(self, current: Duration, previous: Duration) -> float:
        """Calculate the time between contractions"""
        if self._contractions_overlap(current, previous):
            raise ContractionOverlaps()
        return (current.start_time - previous.end_time).total_seconds() / 60

    def _contractions_overlap(self, a: Duration, b: Duration) -> bool:
        """Check if two contractions overlap"""
        return a.start_time <= b.end_time and a.end_time >= b.start_time
