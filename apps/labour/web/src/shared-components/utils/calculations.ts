import { ContractionReadModel } from '@base/clients/labour_service_v2';

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
