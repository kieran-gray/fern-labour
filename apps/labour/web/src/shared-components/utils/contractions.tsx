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
