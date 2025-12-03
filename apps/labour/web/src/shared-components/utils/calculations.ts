import { ContractionDTO } from '@clients/labour_service';

interface ContractionFrequencyGaps {
  previous: number;
  next: number;
}

export const getTimeSinceLastStarted = (
  contractions: ContractionDTO[]
): Record<string, ContractionFrequencyGaps> => {
  const contractionFrequencyGaps: Record<string, ContractionFrequencyGaps> = {};
  let lastStartTime: string = '';
  let previousContractionId: string = '';

  contractions.forEach((contraction) => {
    const frequency = lastStartTime
      ? new Date(contraction.start_time).getTime() - new Date(lastStartTime).getTime()
      : 0;
    const frequencies: ContractionFrequencyGaps = {
      previous: frequency,
      next: 0,
    };
    contractionFrequencyGaps[contraction.id] = frequencies;

    if (previousContractionId) {
      contractionFrequencyGaps[previousContractionId].next = frequency;
    }

    lastStartTime = contraction.start_time;
    previousContractionId = contraction.id;
  });
  return contractionFrequencyGaps;
};

export const secondsElapsed = (contraction: ContractionDTO): number => {
  const timestamp = new Date(contraction.start_time).getTime();
  const now = Date.now();
  return Math.round((now - timestamp) / 1000);
};

export const contractionDurationSeconds = (contraction: ContractionDTO): number => {
  const startTime = new Date(contraction.start_time).getTime();
  const endTime = new Date(contraction.end_time).getTime();
  return Math.round((endTime - startTime) / 1000);
};
