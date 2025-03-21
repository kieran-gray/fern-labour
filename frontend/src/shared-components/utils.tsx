import { ContractionDTO, LabourDTO } from '../client';

interface ContractionFrequencyGaps {
  previous: number;
  next: number;
}

export const dueDateToGestationalAge = (dueDate: Date) => {
  const today = new Date().getTime();
  const resultDate = new Date();
  const fortyWeeksInMs = 40 * 7 * 24 * 60 * 60 * 1000;
  resultDate.setTime(dueDate.getTime() - fortyWeeksInMs);

  const diffInMs = Math.abs(today - resultDate.getTime());
  const totalDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
  const weeks = Math.floor(totalDays / 7);
  const days = totalDays % 7;

  return `${weeks} week${weeks === 0 || weeks > 1 ? 's' : ''} + ${days} day${days === 0 || days > 1 ? 's' : ''}`;
};

export const formatTimeMilliseconds = (milliseconds: number) => {
  if (milliseconds === 0) {
    return null;
  }
  const seconds = Math.floor(milliseconds / 1000);
  return formatTimeSeconds(seconds);
};

export const formatTimeSeconds = (seconds: number): string => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds - h * 3600) / 60);
  const s = Math.floor(seconds - h * 3600 - m * 60);
  const timeString = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  return timeString.startsWith('00') ? timeString.substring(3) : timeString;
};

export const sortContractions = (contractions: ContractionDTO[]): ContractionDTO[] => {
  return contractions.sort((a, b) =>
    a.start_time < b.start_time ? -1 : a.start_time > b.start_time ? 1 : 0
  );
};

export const sortLabours = (labours: LabourDTO[]): LabourDTO[] => {
  return labours.sort((a, b) => (a.due_date < b.due_date ? -1 : a.due_date > b.due_date ? 1 : 0));
};

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

export function pluraliseName(name: string): string {
  return name.endsWith('s') ? `${name}'` : `${name}'s`;
}
