import {
  IconChartHistogram,
  IconMessage,
  IconPencil,
  IconSend,
  IconStopwatch,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Space, Tabs, Text } from '@mantine/core';
import { ApiError, LabourService, OpenAPI } from '../../client';
import { NotFoundError } from '../../Errors';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { LabourProvider } from './LabourContext.tsx';
import { LabourControls } from './Tabs/Details/LabourControls.tsx';
import { SubscribersContainer } from './Tabs/Details/ManageSubscribers/ManageSubscribers.tsx';
import Plan from './Tabs/Details/Plan/Plan.tsx';
import { InviteContainer } from './Tabs/Invites/InviteContainer/InviteContainer.tsx';
import { ShareContainer } from './Tabs/Invites/ShareContainer/ShareContainer.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { Contractions } from './Tabs/Track/Contractions.tsx';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const LabourPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getActiveLabourApiV1LabourActiveGet();
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
          <div className={baseClasses.flexPageColumn}>
            <div style={{ height: '4vh' }} />
            <Plan
              labour={undefined}
              setActiveTab={() => {
                navigate('/');
              }}
            />
          </div>
        </AppShell>
      );
    }
    return (
      <AppShell>
        <ErrorContainer message={error.message} />;
      </AppShell>
    );
  }

  const labour = data;
  return (
    <AppShell>
      <LabourProvider labourId={labour.id}>
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
            <Tabs.Tab value="details" leftSection={<IconPencil />}>
              <Text className={baseClasses.navTabText}>Details</Text>
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
              <Space h="xl" />
              <LabourControls labour={labour} />
              <Space h="xl" />
              <SubscribersContainer />
            </Tabs.Panel>
            <Tabs.Panel value="track">
              <Space h="xl" />
              <Contractions labour={labour} />
            </Tabs.Panel>
            <Tabs.Panel value="stats">
              <Space h="xl" />
              <LabourStatistics labour={labour} completed={false} />
            </Tabs.Panel>
            <Tabs.Panel value="updates">
              <Space h="xl" />
              <LabourUpdates labour={labour} />
            </Tabs.Panel>
            <Tabs.Panel value="invite">
              <Space h="xl" />
              <InviteContainer />
              <Space h="xl" />
              <ShareContainer />
              <Space h="xl" />
            </Tabs.Panel>
          </div>
        </Tabs>
      </LabourProvider>
    </AppShell>
  );
};
