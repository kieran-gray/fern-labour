import { Text } from '@mantine/core';
import { LabourStatisticsDataDTO } from '../../client';
import { formatTimeSeconds } from '../utils';
import classes from './LabourStatistics.module.css';

export const LabourStatisticsTabPanel = ({ data }: { data: LabourStatisticsDataDTO }) => {
  return (
    <>
      <Text className={classes.labourStatsText}>
        Contractions: <strong>{data.contraction_count}</strong>
      </Text>
      <Text className={classes.labourStatsText}>
        Avg contraction duration: <strong>{formatTimeSeconds(data.average_duration)}</strong>
      </Text>
      <Text className={classes.labourStatsText}>
        Avg contraction frequency: <strong>{formatTimeSeconds(data.average_frequency)}</strong>
      </Text>
      <Text className={classes.labourStatsText}>
        Avg contraction intensity:{' '}
        <strong>{data.average_intensity.toPrecision(2)} out of 10</strong>
      </Text>
    </>
  );
};
