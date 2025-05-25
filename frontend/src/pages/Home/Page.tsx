import { LabourPage } from '@labour/Page.tsx';
import { AppShell } from '@shared/AppShell';
import { AppMode, SelectAppMode, useMode } from '../Home/SelectAppMode.tsx';
import { SubscriptionProvider } from '../Subscription/SubscriptionContext.tsx';
import { SubscriptionsPage } from '../Subscriptions/Page.tsx';

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
