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
import { useNavigate } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { Space, Tabs, Text } from '@mantine/core';
import { ApiError, OpenAPI, SubscriptionService } from '../../client/index.ts';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { pluraliseName } from '../../shared-components/utils.tsx';
import { InviteContainer } from '../Subscriptions/Components/InviteContainer/InviteContainer.tsx';
import { SubscriptionsContainer } from '../Subscriptions/Components/ManageSubscriptions/ManageSubscriptions.tsx';
import { useSubscription } from './SubscriptionContext.tsx';
import { Announcements } from './Tabs/Announcements/Announcements.tsx';
import ContactMethods from './Tabs/LabourDetails/ContactMethods.tsx';
import LabourDetails from './Tabs/LabourDetails/LabourDetails.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { StatusUpdates } from './Tabs/StatusUpdates/StatusUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

const TABS = [
  { id: 'subscriptions', label: 'Subscriptions', icon: IconUsers },
  { id: 'details', label: 'Details', icon: IconPencil },
  { id: 'updates', label: 'Updates', icon: IconMessage },
  { id: 'announcements', label: 'Announcements', icon: IconSpeakerphone },
  { id: 'stats', label: 'Stats', icon: IconChartHistogram },
] as const;

const tabOrder = TABS.map((tab) => tab.id);

export const SubscriptionPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const { subscriptionId, setSubscriptionId } = useSubscription();
  const [activeTab, setActiveTab] = useState<string | null>('details');

  if (!subscriptionId) {
    navigate('/subscriptions');
    return null;
  }

  const swipeHandlers = useSwipeable({
    onSwipedRight: () => {
      if (activeTab) {
        const tabIndex = tabOrder.indexOf(activeTab as (typeof tabOrder)[number]);
        if (tabIndex > 0) {
          setActiveTab(tabOrder[tabIndex - 1]);
        }
      }
    },
    onSwipedLeft: () => {
      if (activeTab) {
        const tabIndex = tabOrder.indexOf(activeTab as (typeof tabOrder)[number]);
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

  OpenAPI.TOKEN = async () => auth.user?.access_token || '';

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
        if (err instanceof ApiError && [403, 404].includes(err.status)) {
          // User has been blocked or removed
          // Or Birthing Person has been deleted
          setSubscriptionId('');
          navigate('/');
        }
        throw new Error('Failed to load subscription. Please try again later.');
      }
    },
    refetchInterval: 30000,
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

  const renderTabPanel = (tabId: string) => {
    switch (tabId) {
      case 'subscriptions':
        return (
          <>
            <SubscriptionsContainer />
            <Space h="xl" />
            <InviteContainer />
          </>
        );
      case 'details':
        return (
          <>
            <LabourDetails labour={data.labour} birthingPersonName={pluralisedBirthingPersonName} />
            {data.labour.end_time == null && (
              <>
                <Space h="xl" />
                <ContactMethods subscription={data.subscription} />
              </>
            )}
          </>
        );
      case 'stats':
        return (
          <LabourStatistics
            labour={data.labour}
            birthingPersonName={pluralisedBirthingPersonName}
          />
        );
      case 'updates':
        return <StatusUpdates labour={data.labour} birthingPerson={data.birthing_person} />;
      case 'announcements':
        return (
          <Announcements
            labour={data.labour}
            birthingPersonName={pluralisedBirthingPersonName}
            birthingPerson={data.birthing_person}
          />
        );
      default:
        return null;
    }
  };

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
            {TABS.map((tab) => (
              <Tabs.Tab key={tab.id} value={tab.id} leftSection={<tab.icon />}>
                <Text className={baseClasses.navTabText}>{tab.label}</Text>
              </Tabs.Tab>
            ))}
          </Tabs.List>
          <div className={baseClasses.flexPageColumn}>
            {TABS.map((tab) => (
              <Tabs.Panel key={tab.id} value={tab.id} keepMounted={tab.id !== 'stats'}>
                {renderTabPanel(tab.id)}
              </Tabs.Panel>
            ))}
          </div>
        </Tabs>
      </AppShell>
    </div>
  );
};
