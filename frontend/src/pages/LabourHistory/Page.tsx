import { AppShell } from '../../shared-components/AppShell.tsx';
import { LabourHistory } from './Components/LabourHistory/LabourHistory.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const LabourHistoryPage = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <LabourHistory />
      </div>
    </AppShell>
  );
};
