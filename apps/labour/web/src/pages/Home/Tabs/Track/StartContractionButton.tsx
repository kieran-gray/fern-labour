import { RefObject } from 'react';
import { useLabourSession } from '@base/contexts/LabourSessionContext';
import { useLabourV2Client } from '@base/hooks';
import { generateContractionId, useStartContractionOffline } from '@base/offline/hooks';
import { IconHourglassLow } from '@tabler/icons-react';
import { Button } from '@mantine/core';
import { StopwatchHandle } from './Stopwatch/Stopwatch';

export default function StartContractionButton({
  stopwatchRef,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
}) {
  const { labourId } = useLabourSession();
  const client = useLabourV2Client();
  const mutation = useStartContractionOffline(client);

  const handleStartContraction = () => {
    stopwatchRef.current?.start();

    const contractionId = generateContractionId();
    mutation.mutate({
      labourId: labourId!,
      startTime: new Date(),
      contractionId,
    });
  };

  const icon = <IconHourglassLow size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="filled"
      loading={mutation.isPending}
      color="var(--mantine-primary-color-4)"
      onClick={handleStartContraction}
    >
      Start Contraction
    </Button>
  );
}
