import { RefObject } from 'react';
import { ContractionReadModel } from '@base/clients/labour_service_v2';
import { useLabourSession } from '@base/contexts/LabourSessionContext';
import { useLabourV2Client, useStartContractionV2 } from '@shared/hooks';
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
  const mutation = useStartContractionV2(client);

  const createNewContraction = (): ContractionReadModel => {
    const startTime = new Date().toISOString();
    return {
      contraction_id: 'placeholder',
      labour_id: labourId!,
      duration: { start_time: startTime, end_time: startTime },
      duration_seconds: 0,
      intensity: null,
      created_at: startTime,
      updated_at: startTime,
    };
  };

  const handleStartContraction = (contraction: ContractionReadModel) => {
    stopwatchRef.current?.start();

    mutation.mutate({ labourId: contraction.labour_id, startTime: new Date() }); // todo
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
      onClick={() => handleStartContraction(createNewContraction())}
    >
      Start Contraction
    </Button>
  );
}
