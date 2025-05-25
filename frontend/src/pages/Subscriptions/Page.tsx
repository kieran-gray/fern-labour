import { AppShell } from '@shared/AppShell';
import { useSearchParams } from 'react-router-dom';
import { Space } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { SubscriptionPage } from '../Subscription/Page.tsx';
import { useSubscription } from '../Subscription/SubscriptionContext.tsx';
import { InviteContainer } from './Components/InviteContainer/InviteContainer.tsx';
import { SubscriptionsContainer } from './Components/ManageSubscriptions/ManageSubscriptions.tsx';
import SubscriptionRequestedModal from './Components/SubscriptionRequestedModal/SubscriptionRequestedModal.tsx';
import baseClasses from '@shared/shared-styles.module.css';

export const SubscriptionsPage = () => {
  const { subscriptionId } = useSubscription();
  const [searchParams] = useSearchParams();
  const [opened, { close }] = useDisclosure(false);
  const prompt = searchParams.get('prompt');

  if (subscriptionId) {
    return <SubscriptionPage />;
  }
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <SubscriptionsContainer />
        <Space h="xl" />
        <InviteContainer />
        <SubscriptionRequestedModal opened={opened || prompt === 'requested'} close={close} />
      </div>
    </AppShell>
  );
};
