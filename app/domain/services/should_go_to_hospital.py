from app.domain.labour.constants import (
    CONTRACTIONS_REQUIRED_NULLIPAROUS,
    CONTRACTIONS_REQUIRED_PAROUS,
    LENGTH_OF_CONTRACTIONS_MINUTES,
    TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    TIME_BETWEEN_CONTRACTIONS_PAROUS,
)
from app.domain.labour.entity import Labour


class ShouldGoToHospitalService:
    def should_go_to_hospital(self, labour: Labour) -> bool:
        """
        When to go to the hospital depends on if this is a first labour or not.
        For a first time mum we should wait until contractions are well
        established. This means using the 3-1-1 rule:
        Contractions every 3 minutes, lasting 1 minute each, for 1 hour

        Otherwise we don't want to wait as long and should go to the hospital
        when contractions are once every 5 minutes for 30 minutes.
        """
        required_number_of_contractions = (
            CONTRACTIONS_REQUIRED_NULLIPAROUS
            if labour.first_labour
            else CONTRACTIONS_REQUIRED_PAROUS
        )
        required_time_between_contractions = (
            TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS
            if labour.first_labour
            else TIME_BETWEEN_CONTRACTIONS_PAROUS
        )

        if len(labour.contractions) < required_number_of_contractions:
            return False

        recent_contractions = labour.contractions[-required_number_of_contractions:]

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
