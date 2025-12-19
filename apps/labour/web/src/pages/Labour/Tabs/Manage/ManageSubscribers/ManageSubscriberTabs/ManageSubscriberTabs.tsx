import { SubscriptionReadModel, User } from '@base/clients/labour_service/types';
import { useLabourSession } from '@base/contexts/LabourSessionContext';
import { useLabourV2Client } from '@base/hooks';
import { useLabourSubscriptionsV2, useUsersV2 } from '@base/hooks/useLabourData';
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
  const { labourId } = useLabourSession();
  const client = useLabourV2Client();
  const {
    isPending,
    isError,
    data: subscriptions,
    error,
  } = useLabourSubscriptionsV2(client, labourId!);
  const { isPending: usersPending, data: users = [] } = useUsersV2(client, labourId!);

  if (isPending || usersPending) {
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

  if (subscriptions.length === 0) {
    return (
      <ImportantText message="You don't have any subscribers yet, share invites with loved ones in the invite tab." />
    );
  }

  const subscriberById = Object.fromEntries(
    users.map((user: User) => [
      user.user_id,
      {
        firstName: user.first_name || 'Unknown',
        lastName: user.last_name || '',
        id: user.user_id,
      },
    ])
  );

  const activeSubscriptions: SubscriptionReadModel[] = [];
  const requestedSubscriptions: SubscriptionReadModel[] = [];
  const blockedSubscriptions: SubscriptionReadModel[] = [];
  subscriptions.forEach((sub) => {
    if (sub.status === 'SUBSCRIBED') {
      activeSubscriptions.push(sub);
    } else if (sub.status === 'REQUESTED') {
      requestedSubscriptions.push(sub);
    } else if (sub.status === 'BLOCKED') {
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
