import { Timeline, Text, Space } from '@mantine/core';
import { ContractionDTO } from '../../../../client';
import classes from './ContractionTimeline.module.css';

export default function ContractionTimeline({contractions, contractionGaps}: {contractions: ContractionDTO[], contractionGaps: Record<string, string | null>}) {
    const timelineContractions = contractions.map((contraction) => (
        <Timeline.Item fs="xl" fw={1000} bullet={<Text className={classes.bulletText}>{contraction.intensity}</Text>} key={contraction.id} title="">
            <Space h="lg" />
            {contractionGaps[contraction.id] !== null && <Text className={classes.timelineLabel}>Gap: <strong>{contractionGaps[contraction.id]}</strong></Text>}
            <Text className={classes.timelineLabel}>Duration: <strong>{contraction.duration}</strong></Text>
            {contraction.notes && (
                <Text className={classes.timelineLabel}>{contraction.notes}</Text>
            )}
            <Space h="lg" />
        </Timeline.Item>
      ));
  return (
    <Timeline ml={30} active={timelineContractions.length} lineWidth={6} bulletSize={60} color='var(--mantine-color-pink-4)'>
      {timelineContractions}
    </Timeline>
  )
}