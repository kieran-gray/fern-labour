import {
  IconChartHistogram,
  IconMessage,
  IconPencil,
  IconSend,
  IconStopwatch,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Center, Space, Tabs, Text, Title } from '@mantine/core';
import { ApiError, LabourService, OpenAPI } from '../../client';
import { NotFoundError } from '../../Errors';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import { PageLoadingIcon } from '../../shared-components/PageLoading/Loading.tsx';
import { LabourProvider } from './LabourContext.tsx';
import { LabourControls } from './Tabs/Details/LabourControls.tsx';
import { SubscribersContainer } from './Tabs/Details/ManageSubscribers/ManageSubscribers.tsx';
import { InviteContainer } from './Tabs/Invites/InviteContainer/InviteContainer.tsx';
import { ShareContainer } from './Tabs/Invites/ShareContainer/ShareContainer.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { Contractions } from './Tabs/Track/Contractions.tsx';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const LabourPage = () => {
  const auth = useAuth();

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

  let content = undefined;

  if (isPending) {
    content = (
      <div style={{ margin: 'auto' }}>
        <PageLoadingIcon />
      </div>
    );
  } else if (isError) {
    if (error instanceof NotFoundError) {
      content = (
        <div className={baseClasses.flexColumn}>
          <LabourControls labour={undefined} />
          <div className={baseClasses.root}>
            <div className={baseClasses.header}>
              <Title fz="xl" className={baseClasses.title}>
                Begin Labour
              </Title>
            </div>
            <div className={baseClasses.body}>
              <Text className={baseClasses.text}>You're not currently in active labour.</Text>
              <Text className={baseClasses.text}>Click the button below to begin</Text>
              <Space h="xl" />
              <div className={baseClasses.flexRowEndNoBP} style={{ alignItems: 'stretch' }}>
                TODO REMOVE THIS WHOLE THING
              </div>
            </div>
          </div>
        </div>
      );
    }
    // TODO don't want to do this
    return <ErrorContainer message={error.message} />;
  } else {
    const labour = data;
    content = (
      <LabourProvider labourId={labour.id}>
        <Tabs w="100%" defaultValue="track" radius="lg">
          <Tabs.List grow className={baseClasses.navTabs}>
            <Tabs.Tab className={baseClasses.navTab} value="details" leftSection={<IconPencil />}>
              <Text className={baseClasses.navTabText}>Details</Text>
            </Tabs.Tab>
            <Tabs.Tab className={baseClasses.navTab} value="updates" leftSection={<IconMessage />}>
              <Text className={baseClasses.navTabText}>Updates</Text>
            </Tabs.Tab>
            <Tabs.Tab className={baseClasses.navTab} value="track" leftSection={<IconStopwatch />}>
              <Text className={baseClasses.navTabText}>Track</Text>
            </Tabs.Tab>
            <Tabs.Tab
              className={baseClasses.navTab}
              value="stats"
              leftSection={<IconChartHistogram />}
            >
              <Text className={baseClasses.navTabText}>Stats</Text>
            </Tabs.Tab>
            <Tabs.Tab className={baseClasses.navTab} value="invite" leftSection={<IconSend />}>
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
    );
  }

  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <Center flex="shrink">{content}</Center>
      <Space h="xl" />
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
