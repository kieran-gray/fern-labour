import { AppShell } from '../../shared-components/AppShell.tsx';
import { AppMode, SelectAppMode, useMode } from '../Home/SelectAppMode.tsx';
import { LabourPage } from '../Labour/Page.tsx';
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
