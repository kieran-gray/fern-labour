import { useLabourSession } from '@base/contexts/LabourSessionContext';
import { useLabourV2Client } from '@base/hooks';
import { useEndContractionOffline } from '@base/offline/hooks';
import { IconHourglassHigh } from '@tabler/icons-react';
import { Button } from '@mantine/core';

export default function EndContractionButton({
  intensity,
  disabled,
  contractionId,
}: {
  intensity: number;
  disabled: boolean;
  contractionId: string;
}) {
  const { labourId } = useLabourSession();
  const client = useLabourV2Client();
  const mutation = useEndContractionOffline(client);

  const handleEndContraction = () => {
    mutation.mutate({
      intensity,
      endTime: new Date(),
      labourId: labourId!,
      contractionId,
    });
  };

  const icon = <IconHourglassHigh size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="outline"
      loading={mutation.isPending}
      onClick={handleEndContraction}
      disabled={disabled}
    >
      End Contraction
    </Button>
  );
}
