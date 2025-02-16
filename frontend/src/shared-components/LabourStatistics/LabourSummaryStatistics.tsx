import { Text, Title } from '@mantine/core';
import { LabourSummaryDTO } from '../../client';
import { LabourStatisticsTable } from './LabourStatsticsTable';
import baseClasses from '../shared-styles.module.css';
import classes from './LabourStatistics.module.css';

const formatLabourDurationHours = (hours: number): string => {
  const wholeHours = Math.round(hours);
  if (wholeHours < 1) {
    return 'Less than 1 hour';
  }
  if (wholeHours === 1) {
    return `${wholeHours} hour`;
  }
  return `${wholeHours} hours`;
};

export const LabourSummaryStatistics = ({
  labour,
  inContainer = true,
}: {
  labour: LabourSummaryDTO;
  inContainer?: boolean;
}) => {
  const statistics = (
    <>
      <Text className={classes.labourStatsText}>
        Labour duration: <strong>{formatLabourDurationHours(labour.duration)}</strong>
      </Text>
      <Text className={classes.labourStatsText}>
        Current phase: <strong>{labour.current_phase}</strong>
      </Text>
      <Text className={classes.labourStatsText}>
        Hospital recommended: <strong>{labour.hospital_recommended ? 'Yes' : 'Not yet'}</strong>
      </Text>
      {labour.statistics.total && <LabourStatisticsTable data={labour.statistics.total} />}
    </>
  );
  if (inContainer) {
    return (
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <Title fz="xl" className={baseClasses.title}>
            Your Labour Statistics
          </Title>
        </div>
        <div className={baseClasses.body}>{statistics}</div>
      </div>
    );
  }
  return statistics;
};
