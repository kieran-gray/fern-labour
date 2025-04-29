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
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { Space, Tabs, Text } from '@mantine/core';
import { ApiError, LabourQueriesService, OpenAPI } from '../../client';
import { NotFoundError, PermissionDenied } from '../../Errors';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { PayWall } from '../../shared-components/Paywall/PayWall.tsx';
import { CompletedLabourContainer } from '../CompletedLabour/Page.tsx';
import { useLabour } from './LabourContext.tsx';
import { Share } from './Tabs/Invites/Share.tsx';
import { LabourControls } from './Tabs/Manage/LabourControls.tsx';
import { SubscribersContainer } from './Tabs/Manage/ManageSubscribers/ManageSubscribers.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { Contractions } from './Tabs/Track/Contractions.tsx';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

// Define tab configuration to make it more maintainable
const TABS = [
  { id: 'details', label: 'Manage', icon: IconSettings },
  { id: 'updates', label: 'Updates', icon: IconMessage, requiresPaid: true },
  { id: 'track', label: 'Track', icon: IconStopwatch },
  { id: 'stats', label: 'Stats', icon: IconChartHistogram },
  { id: 'invite', label: 'Invite', icon: IconSend, requiresPaid: true },
] as const;

const tabOrder = TABS.map((tab) => tab.id);

export const LabourPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const { labourId, setLabourId } = useLabour();
  const [searchParams, setSearchParams] = useSearchParams();
  const labourIdParam = searchParams.get('labourId');
  const [activeTab, setActiveTab] = useState<string | null>('track');

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
    trackTouch: true,
    preventScrollOnSwipe: true,
  });

  OpenAPI.TOKEN = async () => auth.user?.access_token || '';

  const getLabourId = (labourId: string | null, labourIdParam: string | null): string | null => {
    if (labourId !== null && labourId !== '') {
      return labourId
    }
    return labourIdParam;
  }

  const {
    isPending,
    isError,
    data: labour,
    error,
  } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        let response;
        const id = getLabourId(labourId, labourIdParam);
        if (id !== null) {
          response = await LabourQueriesService.getLabourById({ labourId: id });
        } else {
          response = await LabourQueriesService.getActiveLabour();
          setLabourId(response.labour.id);
        }
        return response.labour;
      } catch (err) {
        if (err instanceof ApiError) {
          if (err.status === 404) {
            throw new NotFoundError();
          } else if (err.status === 403) {
            searchParams.delete('labourId');
            setSearchParams(searchParams);
            throw new PermissionDenied();
          }
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
      return null;
    }
    return (
      <AppShell>
        <ErrorContainer message={error.message} />
      </AppShell>
    );
  }

  if (labour.payment_plan === null) {
    navigate('/onboarding?step=pay');
    return null;
  }

  const paidFeaturesEnabled = labour.payment_plan !== 'solo';
  const completed = labour.end_time !== null;

  const renderTabPanel = (tabId: string) => {
    switch (tabId) {
      case 'details':
        return (
          <>
            <LabourControls labour={labour} />
            {paidFeaturesEnabled && (
              <>
                <Space h="xl" />
                <SubscribersContainer />
              </>
            )}
          </>
        );
      case 'track':
        return <Contractions labour={labour} />;
      case 'stats':
        return <LabourStatistics labour={labour} />;
      case 'updates':
        return paidFeaturesEnabled ? (
          <LabourUpdates labour={labour} />
        ) : completed ? (
          <CompletedLabourContainer />
        ) : (
          <PayWall />
        );
      case 'invite':
        return completed ? (
          <CompletedLabourContainer />
        ) : paidFeaturesEnabled ? (
          <Share />
        ) : (
          <PayWall />
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
            {TABS.map(({ id, label, icon: Icon }) => (
              <Tabs.Tab key={id} value={id} leftSection={<Icon />}>
                <Text className={baseClasses.navTabText}>{label}</Text>
              </Tabs.Tab>
            ))}
          </Tabs.List>
          <div className={baseClasses.flexPageColumn}>
            {TABS.map(({ id }) => (
              <Tabs.Panel key={id} value={id}>
                {renderTabPanel(id)}
              </Tabs.Panel>
            ))}
          </div>
        </Tabs>
      </AppShell>
    </div>
  );
};
