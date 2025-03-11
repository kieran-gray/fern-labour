import { useState } from 'react';
import {
  IconChartHistogram,
  IconMessage,
  IconSend,
  IconSettings,
  IconStopwatch,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { Space, Tabs, Text } from '@mantine/core';
import { ApiError, LabourService, OpenAPI } from '../../client';
import { NotFoundError } from '../../Errors';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { useLabour } from './LabourContext.tsx';
import { Share } from './Tabs/Invites/Share.tsx';
import { LabourControls } from './Tabs/Manage/LabourControls.tsx';
import { SubscribersContainer } from './Tabs/Manage/ManageSubscribers/ManageSubscribers.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { Contractions } from './Tabs/Track/Contractions.tsx';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

const tabOrder = ['details', 'updates', 'track', 'stats', 'invite'];

export const LabourPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const { setLabourId } = useLabour();
  const [activeTab, setActiveTab] = useState<string | null>('track');

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
    trackMouse: true,
    trackTouch: true,
    preventScrollOnSwipe: true,
  });

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getActiveLabourApiV1LabourActiveGet();
        setLabourId(response.labour.id);
        return response.labour;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          throw new NotFoundError();
        }
        throw new Error('Failed to load labour. Please try again later.');
      }
    },
    retry: 0,
  });

  if (isPending) {
    return (
      <AppShell>
        <PageLoading />
      </AppShell>
    );
  }

  if (isError) {
    if (error instanceof NotFoundError) {
      navigate('/onboarding?step=plan');
    }
    return (
      <AppShell>
        <ErrorContainer message={error.message} />
      </AppShell>
    );
  }

  const labour = data;
  if (labour.payment_plan === null) {
    navigate('/onboarding?step=pay');
  }
  return (
    <div {...swipeHandlers}>
      <AppShell>
        <Tabs
          w="100%"
          defaultValue="track"
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
            <Tabs.Tab value="details" leftSection={<IconSettings />}>
              <Text className={baseClasses.navTabText}>Manage</Text>
            </Tabs.Tab>
            <Tabs.Tab value="updates" leftSection={<IconMessage />}>
              <Text className={baseClasses.navTabText}>Updates</Text>
            </Tabs.Tab>
            <Tabs.Tab value="track" leftSection={<IconStopwatch />}>
              <Text className={baseClasses.navTabText}>Track</Text>
            </Tabs.Tab>
            <Tabs.Tab value="stats" leftSection={<IconChartHistogram />}>
              <Text className={baseClasses.navTabText}>Stats</Text>
            </Tabs.Tab>
            <Tabs.Tab value="invite" leftSection={<IconSend />}>
              <Text className={baseClasses.navTabText}>Invite</Text>
            </Tabs.Tab>
          </Tabs.List>
          <div className={baseClasses.flexPageColumn}>
            <Tabs.Panel value="details">
              <LabourControls labour={labour} />
              <Space h="xl" />
              <SubscribersContainer />
            </Tabs.Panel>
            <Tabs.Panel value="track">
              <Contractions labour={labour} />
            </Tabs.Panel>
            <Tabs.Panel value="stats">
              <LabourStatistics labour={labour} completed={false} />
            </Tabs.Panel>
            <Tabs.Panel value="updates">
              <LabourUpdates labour={labour} />
            </Tabs.Panel>
            <Tabs.Panel value="invite">
              <Share />
            </Tabs.Panel>
          </div>
        </Tabs>
      </AppShell>
    </div>
  );
};
