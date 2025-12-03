import { useState } from 'react';
import { IconPhone } from '@tabler/icons-react';
import { Alert } from '@mantine/core';

export function CallMidwifeAlert() {
  const [showCallMidwifeAlert, setShowCallMidwifeAlert] = useState(true);

  const handleCallMidwifeAlertDismiss = () => {
    setShowCallMidwifeAlert(false);
  };

  if (!showCallMidwifeAlert) {
    return;
  }

  return (
    <Alert
      variant="light"
      color="red"
      radius="lg"
      withCloseButton
      title="Time to call your midwife"
      icon={<IconPhone />}
      onClose={handleCallMidwifeAlertDismiss}
    >
      We think that you should call the midwife urgently, we suggest this because either:
      <br />- one of your contractions lasted longer than 2 minutes
      <br />- you have had 6 or more contractions in a 10 minute period
    </Alert>
  );
}
