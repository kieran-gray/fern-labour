import { Image, Space, Text } from '@mantine/core';
import { ContractionDTO, LabourDTO } from '../../../../clients/labour_service';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { ResponsiveDescription } from '../../../../shared-components/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import { formatTimeSeconds } from '../../../../shared-components/utils';
import { LabourStatisticsTabs } from './LabourStatisticsTabs';
import image from './statistics.svg';
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

  return {
    contraction_count: contractions.length,
    average_duration: avgDuration,
    average_intensity: avgIntensity,
    average_frequency: avgFrequency,
  };
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

interface LabourStatisticsProps {
  labour: LabourDTO;
  inContainer?: boolean;
}

export const LabourStatistics = ({ labour, inContainer = true }: LabourStatisticsProps) => {
  const labourStatistics = createLabourStatistics(labour.contractions);
  const completed = labour.end_time !== null;

  const renderTimingInfo = () => (
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
      {labour.start_time && labour.end_time == null && (
        <Text className={classes.labourStatsText}>
          <strong>Elapsed Time: </strong>
          {formatTimeSeconds((new Date().getTime() - new Date(labour.start_time).getTime()) / 1000)}
        </Text>
      )}
    </div>
  );

  const renderStatisticsContent = () => (
    <>
      {renderTimingInfo()}
      <Space h="sm" />
      {!completed && !labourStatistics.total && (
        <ImportantText message="Not enough data yet, keep tracking." />
      )}
      {completed && !labourStatistics.total && (
        <ImportantText message="You didn't track enough contractions to see statistics." />
      )}
      {labourStatistics.total && (
        <LabourStatisticsTabs labour={labour} statistics={labourStatistics} />
      )}
    </>
  );

  if (!inContainer) {
    return renderStatisticsContent();
  }

  const completedDescription =
    'Here, you can see all the statistics about your contractions during your labour journey.';
  const activeDescription =
    'Here, you can view all of the statistics about your contractions. Useful when discussing labour progress with a midwife or healthcare provider.';
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title="Your labour statistics" />
            <ResponsiveDescription
              description={completed ? completedDescription : activeDescription}
              marginTop={10}
            />
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
            {renderStatisticsContent()}
          </div>
        </div>
      </div>
    </div>
  );
};
