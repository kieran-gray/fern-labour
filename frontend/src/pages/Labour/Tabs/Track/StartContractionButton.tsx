import { RefObject } from 'react';
import { useLabour } from '@base/contexts/LabourContext';
import { ContractionDTO } from '@clients/labour_service';
import { useStartContraction } from '@shared/hooks';
import { IconHourglassLow } from '@tabler/icons-react';
import { Button } from '@mantine/core';
import { StopwatchHandle } from './Stopwatch/Stopwatch';

export default function StartContractionButton({
  stopwatchRef,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
}) {
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

  const handleStartContraction = (contraction: ContractionDTO) => {
    stopwatchRef.current?.start();
    startContractionMutation.mutate(contraction);
  };

  const icon = <IconHourglassLow size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="filled"
      loading={startContractionMutation.isPending}
      color="var(--mantine-primary-color-4)"
      onClick={() => handleStartContraction(createNewContraction())}
    >
      Start Contraction
    </Button>
  );
}
