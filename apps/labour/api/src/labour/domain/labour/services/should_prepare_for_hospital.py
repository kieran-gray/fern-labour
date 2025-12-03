from src.labour.domain.labour.constants import (
    LENGTH_OF_CONTRACTIONS_MINUTES,
    SAMPLE_CONTRACTION_SIZE,
    TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    TIME_BETWEEN_CONTRACTIONS_PAROUS,
)
from src.labour.domain.labour.entity import Labour


class ShouldPrepareForHospitalService:
    def should_prepare_for_hospital(self, labour: Labour) -> bool:
        """
        Based on the same timings as ShouldGoToHospitalService, the difference is this domain
        service bases its decision on the last 4 contractions instead of needing to meet the 3-1-1
        or 5-1-1 patterns for an hour.
        """
        required_time_between_contractions = (
            TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS
            if labour.first_labour
            else TIME_BETWEEN_CONTRACTIONS_PAROUS
        )

        if len(labour.contractions) < SAMPLE_CONTRACTION_SIZE:
            return False

        recent_contractions = labour.contractions[-4:]

        # Check if contractions are consistently 5 minutes apart or less
        for prev, curr in zip(recent_contractions, recent_contractions[1:], strict=False):
            time_between = (curr.start_time - prev.end_time).total_seconds() / 60
            if time_between > required_time_between_contractions:
                return False

        # Check if contractions are lasting about 1 minute
        return all(
            c.duration.duration_minutes >= LENGTH_OF_CONTRACTIONS_MINUTES
            for c in recent_contractions
        )
