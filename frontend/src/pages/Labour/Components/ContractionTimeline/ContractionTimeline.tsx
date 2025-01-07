import { Timeline, Text, Space } from '@mantine/core';
import { ContractionDTO } from '../../../../client';
import classes from './ContractionTimeline.module.css';
import {formatTimeSeconds} from '../../../../shared-components/utils';

export default function ContractionTimeline({contractions, contractionGaps}: {contractions: ContractionDTO[], contractionGaps: Record<string, string | null>}) {
   const formatIntensity = (intensity: number | null): string => {
      return intensity ? intensity.toString() : "0"
   }  

  const timelineContractions = contractions.map((contraction) => (
        <Timeline.Item 
          fs="xl"
          fw={1000}
          bullet={<Text className={classes.bulletText}>{contraction.start_time !== contraction.end_time && formatIntensity(contraction.intensity)}</Text>}
          key={contraction.id} title="">
            <Text className={classes.timelineLabel}>
              Start Time: <strong>{new Date(contraction.start_time).toLocaleTimeString(navigator.language, {"hour": "2-digit", "minute": "2-digit"})}</strong>
            </Text>
            {contractionGaps[contraction.id] !== null &&
              <Text className={classes.timelineLabel}>
                Gap: <strong>{contractionGaps[contraction.id]}</strong>
              </Text>}
            {contraction.start_time !== contraction.end_time &&
              <Text className={classes.timelineLabel}>Duration: <strong>{formatTimeSeconds(contraction.duration)}</strong></Text>}
            {contraction.notes && (
                <Text className={classes.timelineLabel}>{contraction.notes}</Text>
            )}
            <Space h="md" />
        </Timeline.Item>
      ));
  return (
    <Timeline ml={30} active={timelineContractions.length} lineWidth={6} bulletSize={60} color='var(--mantine-color-pink-4)'>
      {timelineContractions}
    </Timeline>
  )
}