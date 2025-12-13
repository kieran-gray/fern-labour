import { useEndContractionV2, useLabourV2Client } from '@shared/hooks';
import { IconHourglassHigh } from '@tabler/icons-react';
import { Button } from '@mantine/core';
import { useLabour } from '@base/contexts/LabourContext';

export default function EndContractionButton({
  intensity,
  disabled,
}: {
  intensity: number;
  disabled: boolean;
}) {
  const { labourId } = useLabour();
  const client = useLabourV2Client();
  const mutation = useEndContractionV2(client);

  const handleEndContraction = ({ intensity, endTime }: { intensity: number; endTime: Date }) => {
    mutation.mutate({ intensity, endTime, labourId: labourId! });
  };

  const icon = <IconHourglassHigh size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="outline"
      loading={mutation.isPending}
      onClick={() => {
        const endTime = new Date();
        handleEndContraction({ intensity, endTime });
      }}
      disabled={disabled}
    >
      End Contraction
    </Button>
  );
}
