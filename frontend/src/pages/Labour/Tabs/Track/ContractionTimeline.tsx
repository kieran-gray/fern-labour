import { useEffect, useRef } from 'react';
import { ScrollArea, Space, Text, Timeline } from '@mantine/core';
import { ContractionDTO } from '../../../../client';
import {
  formatTimeMilliseconds,
  formatTimeSeconds,
  getTimeSinceLastStarted,
} from '../../../../shared-components/utils';
import classes from './Contractions.module.css';

const DOTTED_LINE_FREQUENCY_GAP = 1800000;

export default function ContractionTimeline({ contractions }: { contractions: ContractionDTO[] }) {
  const viewport = useRef<HTMLDivElement>(null);
  const formatIntensity = (intensity: number | null): string => {
    return intensity ? intensity.toString() : '0';
  };
  const contractionFrequencyGaps = getTimeSinceLastStarted(contractions);

  const timelineContractions = contractions.map((contraction) => (
    <Timeline.Item
      fs="xl"
      fw={1000}
      bullet={
        <Text className={classes.bulletText}>
          {contraction.start_time !== contraction.end_time &&
            formatIntensity(contraction.intensity)}
        </Text>
      }
      onClick={() => {
        console.log(contraction.id);
      }}
      key={contraction.id}
      title=""
      lineVariant={
        contractionFrequencyGaps[contraction.id].next > DOTTED_LINE_FREQUENCY_GAP
          ? 'dotted'
          : 'solid'
      }
    >
      <Text className={classes.timelineLabel}>
        Start Time:{' '}
        <strong>
          {new Date(contraction.start_time).toLocaleTimeString(navigator.language, {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </strong>
      </Text>
      {contractionFrequencyGaps[contraction.id].previous !== 0 && (
        <Text className={classes.timelineLabel}>
          Frequency:{' '}
          <strong>
            {formatTimeMilliseconds(contractionFrequencyGaps[contraction.id].previous)}
          </strong>
        </Text>
      )}
      {contraction.start_time !== contraction.end_time && (
        <Text className={classes.timelineLabel}>
          Duration: <strong>{formatTimeSeconds(contraction.duration)}</strong>
        </Text>
      )}
      {contractionFrequencyGaps[contraction.id].previous === 0 && <br />}
      {contraction.notes && <Text className={classes.timelineLabel}>{contraction.notes}</Text>}
      <Space h="md" />
    </Timeline.Item>
  ));

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [timelineContractions]);

  return (
    <ScrollArea.Autosize mah={500} viewportRef={viewport}>
      <Timeline
        ml={30}
        active={timelineContractions.length}
        lineWidth={6}
        bulletSize={60}
        color="var(--mantine-color-pink-4)"
      >
        {timelineContractions}
      </Timeline>
    </ScrollArea.Autosize>
  );
}
