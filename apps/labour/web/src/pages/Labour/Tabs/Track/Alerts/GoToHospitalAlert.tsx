import { useState } from 'react';
import { IconAmbulance } from '@tabler/icons-react';
import { Alert } from '@mantine/core';

export function GoToHospitalAlert() {
  const [showGoToHospitalAlert, setShowGoToHospitalAlert] = useState(true);

  const handleGoToHospitalAlertDismiss = () => {
    setShowGoToHospitalAlert(false);
  };

  if (!showGoToHospitalAlert) {
    return;
  }

  return (
    <Alert
      variant="light"
      color="orange"
      radius="lg"
      withCloseButton
      title="Time to go to the hospital"
      icon={<IconAmbulance />}
      onClose={handleGoToHospitalAlertDismiss}
    >
      Your contractions are regular and strong, which means your labour is well underway.
      <br />
      Take a deep breath, gather your things, and go to the hospital safely.
    </Alert>
  );
}
