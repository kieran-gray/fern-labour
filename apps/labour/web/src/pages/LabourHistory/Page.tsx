import { AppShell } from '@components/AppShell';
import { LabourHistory } from './LabourHistory';
import baseClasses from '@components/shared-styles.module.css';

export const LabourHistoryPage = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <LabourHistory />
      </div>
    </AppShell>
  );
};
