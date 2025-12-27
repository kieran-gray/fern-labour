import { useState } from 'react';
import { ContractionReadModel } from '@base/clients/labour_service/types';
import { AlertType, calculateAlerts } from '@base/utils/contractionAlerts';
import { CallMidwifeAlert } from './CallMidwifeAlert';
import { GoToHospitalAlert } from './GoToHospitalAlert';
import { PrepareForHospitalAlert } from './PrepareForHospital';

type AlertContainerProps = {
  contractions: ContractionReadModel[];
  firstLabour: boolean;
};

export function AlertContainer({ contractions, firstLabour }: AlertContainerProps) {
  const [dismissedAlerts, setDismissedAlerts] = useState<Set<AlertType>>(new Set());

  const alertState = calculateAlerts(contractions, firstLabour);

  const handleDismiss = (alertType: AlertType) => {
    setDismissedAlerts((prev) => new Set(prev).add(alertType));
  };

  const getAlertToShow = (): AlertType | null => {
    if (alertState.callMidwife && !dismissedAlerts.has('callMidwife')) {
      return 'callMidwife';
    }
    if (alertState.goToHospital && !dismissedAlerts.has('goToHospital')) {
      return 'goToHospital';
    }
    if (alertState.prepareForHospital && !dismissedAlerts.has('prepareForHospital')) {
      return 'prepareForHospital';
    }
    return null;
  };

  const alertToShow = getAlertToShow();

  switch (alertToShow) {
    case 'callMidwife':
      return <CallMidwifeAlert onClose={() => handleDismiss('callMidwife')} />;
    case 'goToHospital':
      return <GoToHospitalAlert onClose={() => handleDismiss('goToHospital')} />;
    case 'prepareForHospital':
      return <PrepareForHospitalAlert onClose={() => handleDismiss('prepareForHospital')} />;
    default:
      return null;
  }
}
