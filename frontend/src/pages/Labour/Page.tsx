import { useState } from 'react';
import { NotFoundError, PermissionDenied } from '@base/Errors';
import { useNetworkState } from '@base/offline/sync/networkDetector.ts';
import { AppShell } from '@shared/AppShell';
import { ErrorContainer } from '@shared/ErrorContainer/ErrorContainer.tsx';
import { useCurrentLabour } from '@shared/hooks';
import { PageLoading } from '@shared/PageLoading/PageLoading.tsx';
import {
  IconChartHistogram,
  IconMessage,
  IconSend,
  IconSettings,
  IconStopwatch,
} from '@tabler/icons-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { Space } from '@mantine/core';
import { CompletedLabourContainer } from '../CompletedLabour/Page.tsx';
import { useLabour } from './LabourContext.tsx';
import { Share } from './Tabs/Invites/Share.tsx';
import { LabourControls } from './Tabs/Manage/LabourControls.tsx';
import { SubscribersContainer } from './Tabs/Manage/ManageSubscribers/ManageSubscribers.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { Contractions } from './Tabs/Track/Contractions.tsx';
import { FloatingContractionControls } from './Tabs/Track/FloatingContractionControls.tsx';
import { FloatingLabourUpdateControls } from './Tabs/Updates/FloatingLabourUpdateControls.tsx';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates.tsx';
import baseClasses from '@shared/shared-styles.module.css';

const TABS = [
  { id: 'details', label: 'Manage', icon: IconSettings },
  { id: 'updates', label: 'Updates', icon: IconMessage, requiresPaid: true },
  { id: 'track', label: 'Track', icon: IconStopwatch },
  { id: 'stats', label: 'Stats', icon: IconChartHistogram },
  { id: 'invite', label: 'Invite', icon: IconSend, requiresPaid: true },
] as const;

const tabOrder = TABS.map((tab) => tab.id);

export const LabourPage = () => {
  const navigate = useNavigate();
  const { isOnline } = useNetworkState();
  const { labourId, setLabourId } = useLabour();
  const [searchParams, setSearchParams] = useSearchParams();
  const labourIdParam = searchParams.get('labourId');
  const [activeTab, setActiveTab] = useState<string | null>('track');
  const [isUpdateControlsExpanded, setIsUpdateControlsExpanded] = useState(true);
  const [isContractionControlsExpanded, setIsContractionControlsExpanded] = useState(true);

  const scrollMainToBottom = (smooth: boolean = true) => {
    const main = document.getElementById('app-main');
    if (main) {
      main.scrollTo({ top: main.scrollHeight, behavior: smooth ? 'smooth' : 'auto' });
    }
  };

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

  const getLabourId = (labourId: string | null, labourIdParam: string | null): string | null => {
    if (labourId !== null && labourId !== '') {
      return labourId;
    }
    return labourIdParam;
  };

  const currentLabourId = getLabourId(labourId, labourIdParam);

  const { isPending, isError, data: labour, error } = useCurrentLabour(currentLabourId);

  // Set labour ID if we got it from active labour
  if (labour && !currentLabourId && labour.id !== labourId) {
    setLabourId(labour.id);
  }

  // Handle permission errors by cleaning up URL params
  if (isError && error instanceof PermissionDenied) {
    searchParams.delete('labourId');
    setSearchParams(searchParams);
  }

  if (isPending) {
    return (
      <AppShell>
        <PageLoading />
      </AppShell>
    );
  }

  if (isError) {
    if (error instanceof NotFoundError) {
      navigate('/onboarding');
      return null;
    }
    return (
      <AppShell>
        <ErrorContainer message={error.message} />
      </AppShell>
    );
  }

  const completed = labour.end_time !== null;
  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);

  const getFloatingControlsPadding = () => {
    if (window.innerWidth >= 768 || completed) {
      return '30px';
    }
    if (activeTab === 'track') {
      if (!isContractionControlsExpanded) {
        return '50px';
      }
      return activeContraction ? '350px' : '140px';
    }

    if (activeTab === 'updates') {
      if (isUpdateControlsExpanded) {
        return isOnline ? '265px' : '120px';
      }
      return '55px';
    }
  };

  const renderTabPanel = (tabId: string) => {
    switch (tabId) {
      case 'details':
        return (
          <>
            <LabourControls labour={labour} />
            <Space h="xl" />
            <SubscribersContainer />
          </>
        );
      case 'track':
        return <Contractions labour={labour} />;
      case 'stats':
        return <LabourStatistics labour={labour} />;
      case 'updates':
        return <LabourUpdates labour={labour} />;
      case 'invite':
        return completed ? <CompletedLabourContainer /> : <Share />;
      default:
        return null;
    }
  };

  return (
    <div {...swipeHandlers}>
      <AppShell navItems={TABS} activeNav={activeTab} onNavChange={setActiveTab}>
        {/* Content Area */}
        <div
          className={baseClasses.flexPageColumn}
          style={{ paddingBottom: getFloatingControlsPadding() }}
        >
          <div
            style={{
              width: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            {renderTabPanel(activeTab || 'track')}
          </div>
        </div>

        {/* Floating Contraction Controls */}
        <FloatingContractionControls
          labour={labour}
          activeTab={activeTab}
          onToggle={(expanded) => {
            setIsContractionControlsExpanded(expanded);
            if (expanded) {
              setTimeout(() => scrollMainToBottom(true), 50);
            }
          }}
        />

        {/* Floating Labour Update Controls */}
        <FloatingLabourUpdateControls
          labour={labour}
          activeTab={activeTab}
          onToggle={(expanded) => {
            setIsUpdateControlsExpanded(expanded);
            if (expanded) {
              setTimeout(() => scrollMainToBottom(true), 50);
            }
          }}
        />
      </AppShell>
    </div>
  );
};
