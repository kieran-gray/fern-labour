import { useState } from 'react';
import { NotFoundError, PermissionDenied } from '@base/Errors';
import { AppShell } from '@shared/AppShell';
import { BottomNavigation } from '@shared/BottomNavigation';
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
  const { labourId, setLabourId } = useLabour();
  const [searchParams, setSearchParams] = useSearchParams();
  const labourIdParam = searchParams.get('labourId');
  const [activeTab, setActiveTab] = useState<string | null>('track');
  const [isUpdateControlsExpanded, setIsUpdateControlsExpanded] = useState(true);
  const [isContractionControlsExpanded, setIsContractionControlsExpanded] = useState(true);

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
    // No padding needed on desktop since controls are inline and there's no bottom navigation
    if (window.innerWidth >= 768) {
      // Mantine breakpoint-sm
      return '30px';
    }

    if (completed) {
      return '100px';
    }

    if (activeTab === 'track') {
      if (!isContractionControlsExpanded) {
        return '120px';
      }
      return activeContraction ? '400px' : '200px';
    }

    if (activeTab === 'updates') {
      return isUpdateControlsExpanded ? '320px' : '120px';
    }

    return '100px';
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
          onToggle={setIsContractionControlsExpanded}
        />

        {/* Floating Labour Update Controls */}
        <FloatingLabourUpdateControls
          labour={labour}
          activeTab={activeTab}
          onToggle={setIsUpdateControlsExpanded}
        />

        {/* Mobile Bottom Navigation */}
        <BottomNavigation items={TABS} activeItem={activeTab} onItemChange={setActiveTab} />
      </AppShell>
    </div>
  );
};
