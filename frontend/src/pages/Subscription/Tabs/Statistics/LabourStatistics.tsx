import { IconInfoCircle } from '@tabler/icons-react';
import { Image, Space, Text, Title } from '@mantine/core';
import { LabourDTO } from '../../../../client';
import { formatTimeSeconds } from '../../../../shared-components/utils';
import { createLabourStatistics } from '../../../Labour/Tabs/Statistics/LabourStatistics';
import { LabourStatisticsTabs } from '../../../Labour/Tabs/Statistics/LabourStatisticsTabs';
import { LabourStatisticsTable } from '../../../Labour/Tabs/Statistics/LabourStatsticsTable';
import image from '../../../Labour/Tabs/Statistics/statistics.svg';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from '../../../Labour/Tabs/Statistics/LabourStatistics.module.css';

export const LabourStatistics = ({
  labour,
  birthingPersonName,
}: {
  labour: LabourDTO;
  birthingPersonName: string;
}) => {
  const completed: boolean = labour.start_time !== null && labour.end_time !== null;
  const labourStatistics = createLabourStatistics(labour.contractions);
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
      {!completed && !labourStatistics.total && (
        <Text className={baseClasses.importantText}>
          <IconInfoCircle
            size={20}
            style={{ alignSelf: 'center', marginRight: '10px', flexShrink: 0 }}
          />
          Not enough data yet.
        </Text>
      )}
      {!completed && labourStatistics.total && (
        <LabourStatisticsTabs contractions={labour.contractions} statistics={labourStatistics} />
      )}
      {completed && labourStatistics.total && (
        <LabourStatisticsTable data={labourStatistics.total} />
      )}
    </>
  );
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={3}>{birthingPersonName} labour statistics</Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Here, you can view all of the statistics about {birthingPersonName} contractions. This
              is useful information to have if you are a birth partner and need to discuss{' '}
              {birthingPersonName} labour progress with your midwife or healthcare provider.
            </Text>
            <div className={baseClasses.imageFlexRow}>
                <Image src={image} className={baseClasses.smallImage} />
              </div>
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
};
