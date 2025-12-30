import { ContractionReadModel } from '@base/clients/labour_service/types';

export type AlertType = 'callMidwife' | 'goToHospital' | 'prepareForHospital';

export type AlertState = {
  callMidwife: boolean;
  goToHospital: boolean;
  prepareForHospital: boolean;
};

function getCompletedContractionsSorted(
  contractions: ContractionReadModel[]
): ContractionReadModel[] {
  const completed = contractions.filter((c) => c.duration.start_time !== c.duration.end_time);

  return [...completed].sort(
    (a, b) => new Date(b.duration.start_time).getTime() - new Date(a.duration.start_time).getTime()
  );
}

function startedWithinLastMinutes(contraction: ContractionReadModel, minutes: number): boolean {
  const now = new Date();
  const startTime = new Date(contraction.duration.start_time);
  const minutesAgo = minutes * 60 * 1000; // Convert to milliseconds
  return now.getTime() - startTime.getTime() <= minutesAgo;
}

function checkContractionPattern(
  contractions: ContractionReadModel[],
  requiredCount: number,
  minDurationSeconds: number,
  maxFrequencySeconds: number
): boolean {
  if (contractions.length < requiredCount) {
    return false;
  }

  const subset = contractions.slice(0, requiredCount);

  const allMeetDuration = subset.every((c) => c.duration_seconds >= minDurationSeconds);
  if (!allMeetDuration) {
    return false;
  }

  for (let i = 0; i < subset.length - 1; i++) {
    const current = new Date(subset[i].duration.start_time).getTime();
    const next = new Date(subset[i + 1].duration.start_time).getTime();
    const gapSeconds = (current - next) / 1000;

    if (gapSeconds > maxFrequencySeconds) {
      return false;
    }
  }

  return true;
}

function checkCallMidwife(contractions: ContractionReadModel[]): boolean {
  const hasLongContraction = contractions.some((c) => c.duration_seconds > 120);
  if (hasLongContraction) {
    return true;
  }

  const recentContractions = contractions.filter((c) => startedWithinLastMinutes(c, 10));
  return recentContractions.length >= 6;
}

function checkGoToHospital(contractions: ContractionReadModel[], firstLabour: boolean): boolean {
  if (firstLabour) {
    // Nulliparous: 20 contractions, 60 seconds min, 180 seconds (3 min) max frequency
    return checkContractionPattern(contractions, 20, 60, 180);
  }
  // Parous: 6 contractions, 60 seconds min, 300 seconds (5 min) max frequency
  return checkContractionPattern(contractions, 6, 60, 300);
}

function checkPrepareForHospital(
  contractions: ContractionReadModel[],
  firstLabour: boolean
): boolean {
  if (firstLabour) {
    // Nulliparous: 5 contractions, 60 seconds min, 180 seconds (3 min) max frequency
    return checkContractionPattern(contractions, 5, 60, 180);
  }
  // Parous: 3 contractions, 60 seconds min, 300 seconds (5 min) max frequency
  return checkContractionPattern(contractions, 3, 60, 300);
}

export function calculateAlerts(
  contractions: ContractionReadModel[],
  firstLabour: boolean
): AlertState {
  const sorted = getCompletedContractionsSorted(contractions);

  return {
    callMidwife: checkCallMidwife(sorted),
    goToHospital: checkGoToHospital(sorted, firstLabour),
    prepareForHospital: checkPrepareForHospital(sorted, firstLabour),
  };
}
