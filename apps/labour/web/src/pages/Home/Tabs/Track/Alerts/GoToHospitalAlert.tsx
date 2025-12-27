import { IconAmbulance } from '@tabler/icons-react';
import { Alert } from '@mantine/core';

type GoToHospitalAlertProps = {
  onClose: () => void;
};

export function GoToHospitalAlert({ onClose }: GoToHospitalAlertProps) {
  return (
    <Alert
      variant="light"
      color="orange"
      radius="lg"
      withCloseButton
      title="Time to go to the hospital"
      icon={<IconAmbulance />}
      onClose={onClose}
    >
      Your contractions are regular and strong, which means your labour is well underway.
      <br />
      Take a deep breath, gather your things, and go to the hospital safely.
    </Alert>
  );
}
