import { Space, Text, Title } from '@mantine/core';
import { LabourDTO } from '../../client';
import { ContainerHeader } from '../ContainerHeader/ContainerHeader';
import { formatTimeSeconds } from '../utils';
import { LabourStatisticsTabs } from './LabourStatisticsTabs';
import { LabourStatisticsTable } from './LabourStatsticsTable';
import baseClasses from '../shared-styles.module.css';
import classes from './LabourStatistics.module.css';

export const LabourStatistics = ({
  labour,
  completed,
  inContainer = true,
}: {
  labour: LabourDTO;
  completed: boolean;
  inContainer?: boolean;
}) => {
  const statistics = (
    <>
      <div className={baseClasses.flexRow}>
        <Text className={classes.labourStatsText} mr={10}>
          <strong>Start Time:</strong> {new Date(labour.start_time).toString().slice(0, 21)}
        </Text>
        {(labour.end_time && (
          <>
            <Text className={classes.labourStatsText}>
              <strong>End Time:</strong> {new Date(labour.end_time).toString().slice(0, 21)}
            </Text>
            <Text className={classes.labourStatsText}>
              <strong>Duration: </strong>
              {formatTimeSeconds(
                (new Date(labour.end_time).getTime() - new Date(labour.start_time).getTime()) /
                  1000,
                true
              )}
            </Text>
          </>
        )) || (
          <Text className={classes.labourStatsText}>
            <strong>Elapsed Time: </strong>
            {formatTimeSeconds(
              (new Date().getTime() - new Date(labour.start_time).getTime()) / 1000,
              true
            )}
          </Text>
        )}
      </div>
      <Space h="sm" />
      {!completed && !labour.statistics.total && (
        <Text className={classes.labourStatsText}>Not enough data yet, keep tracking.</Text>
      )}
      {!completed && labour.statistics.total && (
        <LabourStatisticsTabs statistics={labour.statistics} />
      )}
      {completed && labour.statistics.total && (
        <LabourStatisticsTable data={labour.statistics.total} />
      )}
    </>
  );
  if (inContainer) {
    return (
      <div className={baseClasses.root}>
        <ContainerHeader title="Statistics" />
        <div className={baseClasses.body}>
          <div className={classes.inner}>
            <div className={classes.content}>
              <Title order={3}>Your labour statistics</Title>
              <div style={{ marginTop: '20px' }} />
              {statistics}
            </div>
          </div>
        </div>
      </div>
    );
  }
  return statistics;
};
