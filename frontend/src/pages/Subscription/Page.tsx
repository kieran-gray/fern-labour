import { useState } from 'react';
import {
  IconChartHistogram,
  IconMessage,
  IconPencil,
  IconSpeakerphone,
  IconUsers,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useSwipeable } from 'react-swipeable';
import { Space, Tabs, Text } from '@mantine/core';
import { OpenAPI, SubscriptionService } from '../../client/index.ts';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { pluraliseName } from '../../shared-components/utils.tsx';
import { InviteContainer } from '../Subscriptions/Components/InviteContainer/InviteContainer.tsx';
import { SubscriptionsContainer } from '../Subscriptions/Components/ManageSubscriptions/ManageSubscriptions.tsx';
import { useSubscription } from './SubscriptionContext.tsx';
import { Announcements } from './Tabs/Announcements/Announcements.tsx';
import LabourDetails from './Tabs/LabourDetails/LabourDetails.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { StatusUpdates } from './Tabs/StatusUpdates/StatusUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

const tabOrder = ['subscriptions', 'details', 'updates', 'announcements', 'stats'];

export const SubscriptionPage = () => {
  const auth = useAuth();
  const { subscriptionId } = useSubscription();
  const [activeTab, setActiveTab] = useState<string | null>('details');

  if (!subscriptionId) {
    throw new Error('subscriptionId is required');
  }

  const swipeHandlers = useSwipeable({
    onSwipedRight: () => {
      if (activeTab) {
        const tabIndex = tabOrder.indexOf(activeTab);
        if (tabIndex > 0) {
          setActiveTab(tabOrder[tabIndex - 1]);
        }
      }
    },
    onSwipedLeft: () => {
      if (activeTab) {
        const tabIndex = tabOrder.indexOf(activeTab);
        if (tabIndex < tabOrder.length - 1) {
          setActiveTab(tabOrder[tabIndex + 1]);
        }
      }
    },
    delta: 10,
    swipeDuration: 250,
    trackMouse: true,
    trackTouch: true,
    preventScrollOnSwipe: true,
  });

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['subscription_data', subscriptionId, auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response =
          await SubscriptionService.getSubscriptionByIdApiV1SubscriptionSubscriptionDataSubscriptionIdGet(
            {
              subscriptionId,
            }
          );
        return response;
      } catch (err) {
        throw new Error('Failed to load subscription. Please try again later.');
      }
    },
  });

  if (isPending) {
    return (
      <AppShell>
        <PageLoading />
      </AppShell>
    );
  }

  if (isError) {
    return (
      <AppShell>
        <ErrorContainer message={error.message} />
      </AppShell>
    );
  }

  const pluralisedBirthingPersonName = pluraliseName(data.birthing_person.first_name);

  return (
    <div {...swipeHandlers}>
      <AppShell>
        <Tabs
          w="100%"
          defaultValue="details"
          radius="lg"
          classNames={{
            list: baseClasses.navTabs,
            tab: baseClasses.navTab,
            tabSection: baseClasses.navTabSection,
          }}
          value={activeTab}
          onChange={setActiveTab}
        >
          <Tabs.List grow>
            <Tabs.Tab value="subscriptions" leftSection={<IconUsers />}>
              <Text className={baseClasses.navTabText}>Subscriptions</Text>
            </Tabs.Tab>
            <Tabs.Tab value="details" leftSection={<IconPencil />}>
              <Text className={baseClasses.navTabText}>Details</Text>
            </Tabs.Tab>
            <Tabs.Tab value="updates" leftSection={<IconMessage />}>
              <Text className={baseClasses.navTabText}>Updates</Text>
            </Tabs.Tab>
            <Tabs.Tab value="announcements" leftSection={<IconSpeakerphone />}>
              <Text className={baseClasses.navTabText}>Announcements</Text>
            </Tabs.Tab>
            <Tabs.Tab value="stats" leftSection={<IconChartHistogram />}>
              <Text className={baseClasses.navTabText}>Stats</Text>
            </Tabs.Tab>
          </Tabs.List>
          <div className={baseClasses.flexPageColumn}>
            <Tabs.Panel value="subscriptions">
              <SubscriptionsContainer />
              <Space h="xl" />
              <InviteContainer />
            </Tabs.Panel>
            <Tabs.Panel value="details">
              <LabourDetails
                labour={data.labour}
                birthingPersonName={pluralisedBirthingPersonName}
                subscription={data.subscription}
              />
            </Tabs.Panel>
            <Tabs.Panel value="stats" keepMounted={false}>
              <LabourStatistics
                labour={data.labour}
                birthingPersonName={pluralisedBirthingPersonName}
              />
            </Tabs.Panel>
            <Tabs.Panel value="updates">
              <StatusUpdates labour={data.labour} birthingPerson={data.birthing_person} />
            </Tabs.Panel>
            <Tabs.Panel value="announcements">
              <Announcements
                labour={data.labour}
                birthingPersonName={pluralisedBirthingPersonName}
                birthingPerson={data.birthing_person}
              />
            </Tabs.Panel>
          </div>
        </Tabs>
      </AppShell>
    </div>
  );
};
