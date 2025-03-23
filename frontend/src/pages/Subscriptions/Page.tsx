import { useSearchParams } from 'react-router-dom';
import { Space } from '@mantine/core';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { SubscriptionPage } from '../Subscription/Page.tsx';
import { useSubscription } from '../Subscription/SubscriptionContext.tsx';
import { InviteContainer } from './Components/InviteContainer/InviteContainer.tsx';
import { SubscriptionsContainer } from './Components/ManageSubscriptions/ManageSubscriptions.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const SubscriptionsPage = () => {
  const { subscriptionId, setSubscriptionId } = useSubscription();
  const [searchParams, setSearchParams] = useSearchParams();
  const paramSubscriptionId = searchParams.get('subscription');

  if (paramSubscriptionId) {
    setSubscriptionId(paramSubscriptionId);
    searchParams.delete('subscription');
    setSearchParams(searchParams);
  }

  if (subscriptionId) {
    return <SubscriptionPage />;
  }
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <SubscriptionsContainer />
        <Space h="xl" />
        <InviteContainer />
      </div>
    </AppShell>
  );
};
