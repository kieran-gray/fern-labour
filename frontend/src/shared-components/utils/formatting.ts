export const dueDateToGestationalAge = (dueDate: Date) => {
  const today = new Date().getTime();
  const resultDate = new Date();
  const fortyWeeksInMs = 40 * 7 * 24 * 60 * 60 * 1000;
  resultDate.setTime(dueDate.getTime() - fortyWeeksInMs);

  const diffInMs = Math.abs(today - resultDate.getTime());
  const totalDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
  const weeks = Math.floor(totalDays / 7);
  const days = totalDays % 7;

  return `${weeks}w + ${days}d`;
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

export const formatDurationHuman = (totalSeconds: number): string => {
  if (!Number.isFinite(totalSeconds) || totalSeconds <= 0) {
    return '0 seconds';
  }

  const seconds = Math.floor(totalSeconds);
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const parts: string[] = [];

  if (days > 0) {
    parts.push(`${days} day${days === 1 ? '' : 's'}`);
    if (hours > 0) {
      parts.push(`${hours} hour${hours === 1 ? '' : 's'}`);
    }
    return parts.join(' ');
  }

  if (hours > 0) {
    parts.push(`${hours} hour${hours === 1 ? '' : 's'}`);
    if (minutes > 0) {
      parts.push(`${minutes} minute${minutes === 1 ? '' : 's'}`);
    }
    return parts.join(' ');
  }

  if (minutes > 0) {
    return `${minutes} minute${minutes === 1 ? '' : 's'}`;
  }

  return `${secs} second${secs === 1 ? '' : 's'}`;
};

export function pluraliseName(name: string): string {
  return name.endsWith('s') ? `${name}'` : `${name}'s`;
}
