import { RefObject, useState } from 'react';
import { ContractionDTO } from '@clients/labour_service';
import { useLabour } from '@labour/LabourContext';
import { useStartContraction } from '@shared/hooks';
import { IconHourglassLow } from '@tabler/icons-react';
import { Button } from '@mantine/core';
import { StopwatchHandle } from './Stopwatch/Stopwatch';

export default function StartContractionButton({
  stopwatchRef,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
}) {
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const { labourId } = useLabour();
  const startContractionMutation = useStartContraction();

  const createNewContraction = (): ContractionDTO => {
    const startTime = new Date().toISOString();
    return {
      id: 'placeholder',
      labour_id: labourId!,
      start_time: startTime,
      end_time: startTime,
      duration: 0,
      intensity: null,
      notes: null,
      is_active: true,
    };
  };

  const handleStartContraction = async (contraction: ContractionDTO) => {
    setMutationInProgress(true);
    stopwatchRef.current?.start();

    try {
      await startContractionMutation.mutateAsync(contraction);
    } finally {
      setMutationInProgress(false);
    }
  };

  const icon = <IconHourglassLow size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="filled"
      loading={mutationInProgress}
      color="var(--mantine-primary-color-4)"
      onClick={() => handleStartContraction(createNewContraction())}
    >
      Start Contraction
    </Button>
  );
}
