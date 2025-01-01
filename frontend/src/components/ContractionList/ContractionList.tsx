import { Timeline, Text, Space } from '@mantine/core';
import { ContractionDTO } from '../../client';

export default function ContractionList({contractions}: {contractions: ContractionDTO[]}) {
    const timelineContractions = contractions.map((contraction) => (
        <Timeline.Item bullet={contraction.intensity} key={contraction.id} title="">
            <Space h="lg" />
            <Text c="dimmed" size="sm">duration: {contraction.duration}</Text>
            {contraction.notes && (
                <Text c="dimmed" size="sm">{contraction.notes}</Text>
            )}
            <Space h="lg" />
        </Timeline.Item>
      ));
  return (
    <Timeline color="rgba(255, 150, 150, 1)" active={timelineContractions.length} lineWidth={3} bulletSize={50}>
      {timelineContractions}
    </Timeline>
  )
}