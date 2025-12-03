import { LabourDTO } from '@clients/labour_service';
import { createLabourStatistics } from '@labour/Tabs/Statistics/LabourStatistics';
import { LabourStatisticsTabs } from '@labour/Tabs/Statistics/LabourStatisticsTabs';
import image from '@labour/Tabs/Statistics/statistics.svg';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { formatDurationHuman, formatTimeSeconds } from '@shared/utils';
import { Image, Space, Text } from '@mantine/core';
import classes from '@labour/Tabs/Statistics/LabourStatistics.module.css';
import baseClasses from '@shared/shared-styles.module.css';

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
      <div className={classes.statsTextContainer}>
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
                (new Date(labour.end_time).getTime() - new Date(labour.start_time).getTime()) / 1000
              )}
            </Text>
          </>
        )}
        {labour.start_time && (
          <Text className={classes.labourStatsText}>
            <strong>Elapsed Time: </strong>
            {formatDurationHuman(
              (new Date().getTime() - new Date(labour.start_time).getTime()) / 1000
            )}
          </Text>
        )}
      </div>
      <Space h="sm" />
      {!completed && !labourStatistics.total && <ImportantText message="Not enough data yet." />}
      {labourStatistics.total && (
        <LabourStatisticsTabs labour={labour} statistics={labourStatistics} />
      )}
    </>
  );

  const completedDescription = `All the numbers and patterns from ${birthingPersonName} contractions during labour.`;
  const activeDescription = `Here, you can view all of the statistics about ${birthingPersonName} contractions.`;
  const description = completed ? completedDescription : activeDescription;
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={`${birthingPersonName} labour statistics`} />
            <ResponsiveDescription description={description} marginTop={10} />
            <div className={baseClasses.imageFlexRow}>
              <Image src={image} className={baseClasses.smallImage} />
            </div>
          </div>
          <div className={baseClasses.flexColumn}>
            <Image src={image} className={classes.image} />
          </div>
        </div>
        <div className={classes.statsInner}>
          <div className={baseClasses.flexColumn} style={{ width: '100%' }}>
            {statistics}
          </div>
        </div>
      </div>
    </div>
  );
};
