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
  const endContractionMutation = useEndContraction();

  const handleEndContraction = ({ intensity, endTime }: { intensity: number; endTime: string }) => {
    endContractionMutation.mutate({ intensity, endTime });
  };

  const icon = <IconHourglassHigh size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="outline"
      loading={endContractionMutation.isPending}
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
