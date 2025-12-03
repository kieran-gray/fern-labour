import { AppMode, useMode } from '@base/contexts/AppModeContext';
import { SubscriptionProvider } from '@base/contexts/SubscriptionContext';
import { LabourPage } from '@labour/Page';
import { AppShell } from '@shared/AppShell';
import { SubscriptionsPage } from '../Subscriptions/Page';
import { SelectAppMode } from './SelectAppMode';

export const HomePage = () => {
  const { mode } = useMode();
  if (mode === AppMode.Birth) {
    return <LabourPage />;
  }
  if (mode === AppMode.Subscriber) {
    return (
      <SubscriptionProvider>
        <SubscriptionsPage />
      </SubscriptionProvider>
    );
  }
  return (
    <AppShell>
      <SelectAppMode />
    </AppShell>
  );
};
