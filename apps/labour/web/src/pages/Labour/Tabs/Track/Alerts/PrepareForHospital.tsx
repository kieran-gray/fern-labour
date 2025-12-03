import { useState } from 'react';
import { IconBackpack } from '@tabler/icons-react';
import { Alert } from '@mantine/core';

export function PrepareForHospitalAlert() {
  const [showPrepareForHospitalAlert, setShowPrepareForHospitalAlert] = useState(true);

  const handlePrepareForHospitalAlertDismiss = () => {
    setShowPrepareForHospitalAlert(false);
  };

  if (!showPrepareForHospitalAlert) {
    return;
  }

  return (
    <Alert
      variant="light"
      color="orange"
      radius="lg"
      withCloseButton
      title="Prepare to go to the hospital"
      icon={<IconBackpack />}
      onClose={handlePrepareForHospitalAlertDismiss}
    >
      Your contractions are becoming more consistent.
      <br />
      If they remain this strong and frequent for an hour, it will be time to go to the hospital.
      <br />
      Stay relaxed and keep monitoring.
    </Alert>
  );
}
