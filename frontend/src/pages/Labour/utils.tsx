import { ContractionDTO } from "../../client";


export const formatTimeGap = (milliseconds: number) => {
    if (milliseconds === 0) {
      return null
    }
    const seconds = Math.floor(milliseconds / 1000);
    if (seconds < 60) {
      return `${seconds} seconds`
    }
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60;
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
      timeSinceLastEnded[contraction.id] = formatTimeGap(gap)
      lastEndTime = contraction.end_time;
    });
    return timeSinceLastEnded
}

export const secondsElapsed = (contraction: ContractionDTO): number => {
    const timestamp = new Date(contraction.start_time).getTime();
    const now = Date.now();
    return Math.floor((now - timestamp) / 1000);
}
