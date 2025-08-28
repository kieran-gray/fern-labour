import { useState } from 'react';
import { useEndContraction } from '@shared/hooks';
import { IconHourglassHigh } from '@tabler/icons-react';
import { Button } from '@mantine/core';

export default function EndContractionButton({
  intensity,
  disabled,
}: {
  intensity: number;
  disabled: boolean;
}) {
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const endContractionMutation = useEndContraction();

  const handleEndContraction = async ({
    intensity,
    endTime,
  }: {
    intensity: number;
    endTime: string;
  }) => {
    setMutationInProgress(true);

    try {
      await endContractionMutation.mutateAsync({ intensity, endTime });
    } finally {
      setMutationInProgress(false);
    }
  };

  const icon = <IconHourglassHigh size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="white"
      loading={mutationInProgress}
      onClick={() => {
        const endTime = new Date().toISOString();
        handleEndContraction({ intensity, endTime });
      }}
      disabled={disabled}
    >
      End Contraction
    </Button>
  );
}
