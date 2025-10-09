import { useSubscription } from '@base/contexts/SubscriptionContext';
import { AppShell } from '@shared/AppShell';
import { useSearchParams } from 'react-router-dom';
import { Space } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { SubscriptionPage } from '../Subscription/Page';
import { InviteContainer } from './Components/InviteContainer/InviteContainer';
import { SubscriptionsContainer } from './Components/ManageSubscriptions/ManageSubscriptions';
import SubscriptionRequestedModal from './Components/SubscriptionRequestedModal/SubscriptionRequestedModal';
import baseClasses from '@shared/shared-styles.module.css';

export const SubscriptionsPage = () => {
  const { subscriptionId } = useSubscription();
  const [searchParams] = useSearchParams();
  const [opened, { close }] = useDisclosure(false);
  const prompt = searchParams.get('prompt');

  if (subscriptionId) {
    return (
      <>
        <SubscriptionPage />
        <SubscriptionRequestedModal opened={opened || prompt === 'requested'} close={close} />
      </>
    );
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
