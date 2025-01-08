import { ContractionDTO } from "../client";


export const formatTimeMilliseconds = (milliseconds: number) => {
    if (milliseconds === 0) {
      return null
    }
    const seconds = Math.floor(milliseconds / 1000);
    return formatTimeSeconds(seconds)
}

export const formatTimeSeconds = (seconds: number, withHours: boolean = false): string => {
  const secondsString = (seconds: number): string => {
    return `${seconds} second${seconds == 1 ? '' : 's'}`
  }
  const minutesString = (minutes: number): string => {
    return `${minutes} minute${minutes == 1 ? '' : 's'}`
  }
  const hoursString = (hours: number): string => {
    return `${hours} hour${hours == 1 ? '': 's'}`
  }

  const wholeSeconds = Math.floor(seconds);
  if (wholeSeconds < 60) {
    return secondsString(wholeSeconds)
  }
  const minutes = Math.floor(wholeSeconds / 60)
  const remainingSeconds = wholeSeconds % 60;

  if (withHours) {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hoursString(hours)} ${minutesString(remainingMinutes)} ${secondsString(remainingSeconds)}`
  }

  return `${minutesString(minutes)} ${secondsString(remainingSeconds)}`;
}

export const sortContractions = (contractions: ContractionDTO[]): ContractionDTO[] => {
    return contractions.sort(
        (a,b) => (a.start_time < b.start_time) ? -1 : ((a.start_time > b.start_time) ? 1 : 0)
      );
}

export const getTimeSinceLastStarted = (contractions: ContractionDTO[]): Record<string, string | null> => {
    const timeSinceLastStarted: Record<string, string | null> = {};
    let lastStartTime: string = "";
  
    contractions.forEach(contraction => {
      const frequency = lastStartTime ? 
        new Date(contraction.start_time).getTime() - new Date(lastStartTime).getTime() : 0;
      timeSinceLastStarted[contraction.id] = formatTimeMilliseconds(frequency)
      lastStartTime = contraction.end_time;
    });
    return timeSinceLastStarted
}

export const secondsElapsed = (contraction: ContractionDTO): number => {
    const timestamp = new Date(contraction.start_time).getTime();
    const now = Date.now();
    return Math.round((now - timestamp) / 1000);
}