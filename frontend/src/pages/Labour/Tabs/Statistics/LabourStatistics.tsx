import { Image, Space, Text, Title } from '@mantine/core';
import { LabourDTO } from '../../../../client';
import { ContainerHeader } from '../../../../shared-components/ContainerHeader/ContainerHeader';
import { formatTimeSeconds } from '../../../../shared-components/utils';
import image from './image.svg';
import { LabourStatisticsTabs } from './LabourStatisticsTabs';
import { LabourStatisticsTable } from './LabourStatsticsTable';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
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
        {labour.start_time && (
          <Text className={classes.labourStatsText} mr={10}>
            <strong>Start Time:</strong> {new Date(labour.start_time).toString().slice(0, 21)}
          </Text>
        )}

        {labour.start_time && labour.end_time && (
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
        )}
        {labour.start_time && (
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
              <Text c="var(--mantine-color-gray-7)" mt="md">
                Here, you can view all of the statistics about your contractions. This is useful
                information to have when discussing your labour progress with your midwife or
                healthcare provider.
              </Text>
            </div>
            <div className={baseClasses.flexColumn}>
              <Image src={image} className={classes.image} />
            </div>
          </div>
          <div
            className={classes.inner}
            style={{ paddingTop: '0', marginTop: '10px', marginBottom: '10px', width: '100%' }}
          >
            <div className={baseClasses.flexColumn} style={{ width: '100%' }}>
              {statistics}
            </div>
          </div>
        </div>
      </div>
    );
  }
  return statistics;
};
