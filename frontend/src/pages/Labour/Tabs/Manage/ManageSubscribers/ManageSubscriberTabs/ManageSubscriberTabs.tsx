import { useLabour } from '@base/pages/Labour/LabourContext';
import { SubscriptionDTO } from '@clients/labour_service';
import { useLabourSubscriptions } from '@shared/hooks';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { PageLoadingIcon } from '@shared/PageLoading/Loading';
import { IconUserCheck, IconUserOff, IconUserQuestion } from '@tabler/icons-react';
import { Tabs, Text } from '@mantine/core';
import { SubscribersTable } from '../SubscribersTable/SubscribersTable';
import baseClasses from '@shared/shared-styles.module.css';

const TABS = [
  { id: 'subscribed', label: 'Subscribed', icon: IconUserCheck, requiresPaid: true },
  { id: 'requested', label: 'Requested', icon: IconUserQuestion },
  { id: 'blocked', label: 'Blocked', icon: IconUserOff },
] as const;

export const ManageSubscribersTabs = () => {
  const { labourId } = useLabour();
  const { isPending, isError, data, error } = useLabourSubscriptions(labourId!);

  if (isPending) {
    return (
      <div style={{ display: 'flex', width: '100%', justifyContent: 'center' }}>
        <PageLoadingIcon />
      </div>
    );
  }

  if (isError) {
    return (
      <div style={{ display: 'flex', width: '100%', justifyContent: 'center' }}>
        <Text>Something went wrong... {error ? error.message : ''}</Text>
      </div>
    );
  }

  if (data.subscriptions.length === 0) {
    return (
      <ImportantText message="You don't have any subscribers yet, share invites with loved ones in the invite tab." />
    );
  }

  const subscriberById = Object.fromEntries(
    data.subscribers.map((subscriber) => [subscriber.id, subscriber])
  );
  const activeSubscriptions: SubscriptionDTO[] = [];
  const requestedSubscriptions: SubscriptionDTO[] = [];
  const blockedSubscriptions: SubscriptionDTO[] = [];
  data.subscriptions.forEach((sub) => {
    if (sub.status === 'subscribed') {
      activeSubscriptions.push(sub);
    } else if (sub.status === 'requested') {
      requestedSubscriptions.push(sub);
    } else if (sub.status === 'blocked') {
      blockedSubscriptions.push(sub);
    }
  });

  const renderTabPanel = (tabId: string) => {
    switch (tabId) {
      case 'requested':
        return (
          <SubscribersTable
            subscriptions={requestedSubscriptions}
            subscriberById={subscriberById}
            status="requested"
          />
        );
      case 'subscribed':
        return (
          <SubscribersTable
            subscriptions={activeSubscriptions}
            subscriberById={subscriberById}
            status="subscribed"
          />
        );
      case 'blocked':
        return (
          <SubscribersTable
            subscriptions={blockedSubscriptions}
            subscriberById={subscriberById}
            status="blocked"
          />
        );
      default:
        return null;
    }
  };

  return (
    <Tabs
      w="100%"
      defaultValue={requestedSubscriptions.length > 0 ? 'requested' : 'subscribed'}
      radius="lg"
      classNames={{
        tab: baseClasses.navTab,
        tabSection: baseClasses.navTabSection,
      }}
    >
      <Tabs.List grow>
        {TABS.map(({ id, label, icon: Icon }) => (
          <Tabs.Tab key={id} value={id} leftSection={<Icon />}>
            <Text className={baseClasses.navTabText}>{label}</Text>
          </Tabs.Tab>
        ))}
      </Tabs.List>
      {TABS.map(({ id }) => (
        <Tabs.Panel key={id} value={id}>
          {renderTabPanel(id)}
        </Tabs.Panel>
      ))}
    </Tabs>
  );
};
