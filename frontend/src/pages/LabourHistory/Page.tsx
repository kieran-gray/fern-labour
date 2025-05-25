import { AppShell } from '@shared/AppShell';
import { LabourHistory } from './Components/LabourHistory/LabourHistory.tsx';
import baseClasses from '@shared/shared-styles.module.css';

export const LabourHistoryPage = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <LabourHistory />
      </div>
    </AppShell>
  );
};
