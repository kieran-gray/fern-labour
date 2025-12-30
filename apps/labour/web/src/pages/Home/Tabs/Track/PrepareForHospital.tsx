import { IconBackpack } from '@tabler/icons-react';
import { Alert } from '@mantine/core';

type PrepareForHospitalAlertProps = {
  onClose: () => void;
};

export function PrepareForHospitalAlert({ onClose }: PrepareForHospitalAlertProps) {
  return (
    <Alert
      variant="light"
      color="orange"
      radius="lg"
      withCloseButton
      title="Prepare to go to the hospital"
      icon={<IconBackpack />}
      onClose={onClose}
    >
      Your contractions are becoming more consistent.
      <br />
      If they remain this strong and frequent for an hour, it will be time to go to the hospital.
      <br />
      Stay relaxed and keep monitoring.
    </Alert>
  );
}
