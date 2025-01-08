import { AnnouncementDTO, ContractionDTO } from "../client";


export const formatTimeMilliseconds = (milliseconds: number) => {
    if (milliseconds === 0) {
      return null
    }
    const seconds = Math.floor(milliseconds / 1000);
    return formatTimeSeconds(seconds)
}

export const formatTimeSeconds = (seconds: number): string => {
  const wholeSeconds = Math.floor(seconds);
  if (wholeSeconds < 60) {
    if (wholeSeconds == 1) {
      return `${wholeSeconds} second`
    }
    return `${wholeSeconds} seconds`
  }
  const minutes = Math.floor(wholeSeconds / 60)
  const remainingSeconds = wholeSeconds % 60;
  return `${minutes} minute${minutes > 1 ? 's' : ''} ${remainingSeconds} seconds`;
}

export const sortContractions = (contractions: ContractionDTO[]): ContractionDTO[] => {
    return contractions.sort(
        (a,b) => (a.start_time < b.start_time) ? -1 : ((a.start_time > b.start_time) ? 1 : 0)
      );
}

export const getTimeSinceLastEnded = (contractions: ContractionDTO[]): Record<string, string | null> => {
    const timeSinceLastEnded: Record<string, string | null> = {};
    let lastEndTime: string = "";
  
    contractions.forEach(contraction => {
      const gap = lastEndTime ? 
        new Date(contraction.start_time).getTime() - new Date(lastEndTime).getTime() : 0;
      timeSinceLastEnded[contraction.id] = formatTimeMilliseconds(gap)
      lastEndTime = contraction.end_time;
    });
    return timeSinceLastEnded
}

export const secondsElapsed = (contraction: ContractionDTO): number => {
    const timestamp = new Date(contraction.start_time).getTime();
    const now = Date.now();
    return Math.round((now - timestamp) / 1000);
}