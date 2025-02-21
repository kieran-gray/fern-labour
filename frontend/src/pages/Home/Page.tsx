import { AppShell } from '../../shared-components/AppShell.tsx';
import { AppMode, SelectAppMode, useMode } from '../Home/SelectAppMode.tsx';
import { LabourPage } from '../Labour/Page.tsx';

export const HomePage = () => {
  const { mode } = useMode();
  if (mode === AppMode.Birth) {
    return <LabourPage />;
  }
  if (mode === AppMode.Subscriber) {
    return (
      <AppShell>
        <div>Some custom subscriber UI</div>
      </AppShell>
    );
  }
  return (
    <AppShell>
      <SelectAppMode />;
    </AppShell>
  );
};
