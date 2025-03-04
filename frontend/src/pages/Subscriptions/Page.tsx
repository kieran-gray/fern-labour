import { AppShell } from '../../shared-components/AppShell.tsx';
import { SubscriptionPage } from '../Subscription/Page.tsx';
import { useSubscription } from '../Subscription/SubscriptionContext.tsx';
import { SubscriptionsContainer } from './Components/ManageSubscriptions/ManageSubscriptions.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const SubscriptionsPage = () => {
  const { subscriptionId } = useSubscription();

  if (subscriptionId) {
    return <SubscriptionPage />;
  }
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <SubscriptionsContainer />
      </div>
    </AppShell>
  );
};
