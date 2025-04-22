from datetime import UTC, datetime, timedelta

from src.labour.domain.contraction.constants import (
    CONTRACTION_MAX_IN_10_MINS,
    CONTRACTION_MAX_TIME_SECONDS,
)
from src.labour.domain.labour.entity import Labour


class ShouldCallMidwifeUrgentlyService:
    def should_call_midwife_urgently(self, labour: Labour) -> bool:
        """
        https://www.nhs.uk/pregnancy/labour-and-birth/what-happens/the-stages-of-labour-and-birth/
        Call your midwife or maternity unit urgently if:
           - your waters break
           - you have vaginal bleeding
           - your baby is moving less than usual
           - you're less than 37 weeks pregnant and think you might be in labour
           - any of your contractions last longer than 2 minutes
           - you're having 6 or more contractions every 10 minutes
        """
        contractions_in_last_10_mins = []
        for contraction in labour.contractions:
            if contraction.duration.duration_seconds > CONTRACTION_MAX_TIME_SECONDS:
                return True

            if contraction.start_time >= datetime.now(UTC) - timedelta(minutes=10):
                contractions_in_last_10_mins.append(contraction)

        return True if len(contractions_in_last_10_mins) >= CONTRACTION_MAX_IN_10_MINS else False
