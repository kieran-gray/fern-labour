import { IconInfoCircle } from '@tabler/icons-react';
import { Image, Space, Text, Title } from '@mantine/core';
import { ContractionDTO, LabourDTO } from '../../../../client';
import { ContainerHeader } from '../../../../shared-components/ContainerHeader/ContainerHeader';
import { formatTimeSeconds } from '../../../../shared-components/utils';
import image from './image.svg';
import { LabourStatisticsTabs } from './LabourStatisticsTabs';
import { LabourStatisticsTable } from './LabourStatsticsTable';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './LabourStatistics.module.css';

export interface LabourStatisticsData {
  contraction_count: number;
  average_duration: number;
  average_intensity: number;
  average_frequency: number;
}

export interface LabourStatistics {
  last_30_mins?: LabourStatisticsData;
  last_60_mins?: LabourStatisticsData;
  total?: LabourStatisticsData;
}

function isRecentDate(date: Date, minutes: 30 | 60): boolean {
  const now = new Date();
  const diffInMs = now.getTime() - date.getTime();
  const diffInMinutes = diffInMs / (1000 * 60);

  return diffInMinutes <= minutes;
}

export function filterContractions(
  contractions: ContractionDTO[],
  minutes: 30 | 60
): ContractionDTO[] {
  return contractions.filter((contraction) =>
    isRecentDate(new Date(contraction.start_time), minutes)
  );
}

function generateStatisticsData(contractions: ContractionDTO[]): LabourStatisticsData {
  const contractionIntensities: number[] = [];
  const contractionDurations: number[] = [];
  const contractionFrequencies: number[] = [];

  contractions.forEach((contraction) => {
    if (contraction.duration > 0) {
      contractionDurations.push(contraction.duration);
    }
    if (contraction.intensity !== null) {
      contractionIntensities.push(contraction.intensity);
    }
  });

  let avgDuration = 0.0;
  if (contractionDurations.length > 0) {
    const sumDurations = contractionDurations.reduce((sum, duration) => sum + duration, 0);
    avgDuration = sumDurations / contractionDurations.length;
  }

  let avgIntensity = 0.0;
  if (contractionIntensities.length > 0) {
    const sumIntensities = contractionIntensities.reduce((sum, intensity) => sum + intensity, 0);
    avgIntensity = sumIntensities / contractionIntensities.length;
  }

  let avgFrequency = 0.0;
  for (let i = 0; i < contractions.length - 1; i++) {
    const curr = contractions[i + 1];
    const prev = contractions[i];

    const frequency =
      (new Date(curr.start_time).getTime() - new Date(prev.start_time).getTime()) / 1000;
    contractionFrequencies.push(frequency);
  }
  if (contractionFrequencies.length > 0) {
    const sumFrequencies = contractionFrequencies.reduce((sum, freq) => sum + freq, 0);
    avgFrequency = sumFrequencies / contractionFrequencies.length;
  }

  const statistics: LabourStatisticsData = {
    contraction_count: contractions.length,
    average_duration: avgDuration,
    average_intensity: avgIntensity,
    average_frequency: avgFrequency,
  };
  return statistics;
}

export function createLabourStatistics(contractions: ContractionDTO[]): LabourStatistics {
  const statistics: LabourStatistics = {};

  if (contractions.length < 3) {
    return statistics;
  }

  const contractions30Mins = filterContractions(contractions, 30);
  if (contractions30Mins.length > 0) {
    statistics.last_30_mins = generateStatisticsData(contractions30Mins);
  }

  const contractions60Mins = filterContractions(contractions, 60);
  if (contractions60Mins.length > 0) {
    statistics.last_60_mins = generateStatisticsData(contractions60Mins);
  }

  statistics.total = generateStatisticsData(contractions);
  return statistics;
}

export const LabourStatistics = ({
  labour,
  completed,
  inContainer = true,
}: {
  labour: LabourDTO;
  completed: boolean;
  inContainer?: boolean;
}) => {
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
          Not enough data yet, keep tracking.
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
