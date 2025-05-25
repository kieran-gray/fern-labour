import { ContractionDTO } from '@clients/labour_service';
import { ScatterChart } from '@mantine/charts';
import classes from './LabourStatistics.module.css';

interface ChartData {
  color: string;
  name: string;
  data: Record<string, number>[];
}

function getTimestampMinutesAgo(date: Date, minutes: number): number {
  date.setMinutes(date.getMinutes() - minutes);
  return date.getTime();
}

export const LabourStatisticsChart = ({
  contractions,
  minutes,
  endTime,
}: {
  contractions: ContractionDTO[];
  minutes?: number;
  endTime?: Date;
}) => {
  let minStartTime: number | null = null;
  const chartData: ChartData = {
    color: 'var(--mantine-primary-color-6)',
    name: 'Contraction',
    data: [],
  };
  contractions.forEach((contraction) => {
    const startTime = new Date(contraction.start_time).getTime();
    minStartTime =
      minStartTime === null || (minStartTime && startTime < minStartTime)
        ? startTime
        : minStartTime;
    chartData.data.push({
      time: startTime,
      duration: contraction.duration,
    });
  });
  const now = new Date();
  const startTime = minutes
    ? getTimestampMinutesAgo(now, minutes)
    : minStartTime
      ? minStartTime - 100000
      : 0;
  const endX = endTime ? endTime.getTime() : now.getTime();
  return (
    <ScatterChart
      h={350}
      w="100%"
      data={[chartData]}
      dataKey={{ x: 'time', y: 'duration' }}
      xAxisLabel="Time"
      yAxisLabel="Duration (s)"
      xAxisProps={{ domain: [startTime, endX] }}
      valueFormatter={{
        x: (value) => `${new Date(value).toTimeString().slice(0, 5)}`,
        y: (value) => `${value}s`,
      }}
      classNames={{
        root: classes.labourStatsChartRoot,
        axisLabel: classes.labourStatsChartAxisLabel,
      }}
    />
  );
};
