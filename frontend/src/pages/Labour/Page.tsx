import {
  IconChartHistogram,
  IconMessage,
  IconSend,
  IconSettings,
  IconStopwatch,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Space, Tabs, Text } from '@mantine/core';
import { ApiError, LabourService, OpenAPI } from '../../client';
import { NotFoundError } from '../../Errors';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { LabourHistory } from '../LabourHistory/Components/LabourHistory/LabourHistory.tsx';
import { LabourHistoryPage } from '../LabourHistory/Page.tsx';
import { useLabour } from './LabourContext.tsx';
import { InviteContainer } from './Tabs/Invites/InviteContainer/InviteContainer.tsx';
import { ShareContainer } from './Tabs/Invites/ShareContainer/ShareContainer.tsx';
import { LabourControls } from './Tabs/Manage/LabourControls.tsx';
import { SubscribersContainer } from './Tabs/Manage/ManageSubscribers/ManageSubscribers.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { Contractions } from './Tabs/Track/Contractions.tsx';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const LabourPage = () => {
  const auth = useAuth();
  const { setLabourId } = useLabour();

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
      return (
        <AppShell>
          <LabourHistoryPage />
        </AppShell>
      );
    }
    return (
      <AppShell>
        <ErrorContainer message={error.message} />
      </AppShell>
    );
  }

  const labour = data;
  return (
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
            <Space h="xl" />
            <LabourHistory />
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
            <InviteContainer />
            <Space h="xl" />
            <ShareContainer />
            <Space h="xl" />
          </Tabs.Panel>
        </div>
      </Tabs>
    </AppShell>
  );
};
