import { ContractionReadModel } from '@base/clients/labour_service';

interface ContractionFrequencyGaps {
  previous: number;
  next: number;
}

export const getTimeSinceLastStarted = (
  contractions: ContractionReadModel[]
): Record<string, ContractionFrequencyGaps> => {
  const contractionFrequencyGaps: Record<string, ContractionFrequencyGaps> = {};
  let lastStartTime: string = '';
  let previousContractionId: string = '';

  contractions.forEach((contraction) => {
    const frequency = lastStartTime
      ? new Date(contraction.duration.start_time).getTime() - new Date(lastStartTime).getTime()
      : 0;
    const frequencies: ContractionFrequencyGaps = {
      previous: frequency,
      next: 0,
    };
    contractionFrequencyGaps[contraction.contraction_id] = frequencies;

    if (previousContractionId) {
      contractionFrequencyGaps[previousContractionId].next = frequency;
    }

    lastStartTime = contraction.duration.start_time;
    previousContractionId = contraction.contraction_id;
  });
  return contractionFrequencyGaps;
};

export const secondsElapsed = (contraction: ContractionReadModel): number => {
  const timestamp = new Date(contraction.duration.start_time).getTime();
  const now = Date.now();
  return Math.round((now - timestamp) / 1000);
};

export const contractionDurationSeconds = (contraction: ContractionReadModel): number => {
  const startTime = new Date(contraction.duration.start_time).getTime();
  const endTime = new Date(contraction.duration.end_time).getTime();
  return Math.round((endTime - startTime) / 1000);
};

/**
 * Updates the time portion of a datetime string while keeping the date closest to the original.
 * Handles midnight crossings by checking adjacent days.
 */
export const updateTime = (dateTime: string, time: string) => {
  const originalDate = new Date(dateTime);
  const [hours, minutes, seconds] = time.split(':').map(Number);

  const candidates = [];

  for (let dayOffset = -1; dayOffset <= 1; dayOffset++) {
    const candidate = new Date(originalDate);
    candidate.setDate(candidate.getDate() + dayOffset);
    candidate.setHours(hours, minutes, seconds, 0);
    candidates.push(candidate);
  }

  const closest = candidates.reduce((closest, current) => {
    const closestDiff = Math.abs(closest.getTime() - originalDate.getTime());
    const currentDiff = Math.abs(current.getTime() - originalDate.getTime());
    return currentDiff < closestDiff ? current : closest;
  });

  return closest.toISOString();
};
