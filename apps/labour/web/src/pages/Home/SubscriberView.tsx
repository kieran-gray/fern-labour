import { useEffect, useMemo, useState } from 'react';
import { SubscriberRole } from '@base/clients/labour_service';
import { SubscriberSessionState, useLabourSession } from '@base/contexts/LabourSessionContext';
import { useLabourV2Client } from '@base/hooks';
import { flattenContractions, useContractionsInfinite } from '@base/hooks/useInfiniteQueries';
import { useLabourByIdV2, useUserSubscriptionV2 } from '@base/hooks/useLabourData';
import { useNetworkState } from '@base/offline/sync/networkDetector';
import { AppShell } from '@shared/AppShell';
import { ErrorContainer } from '@shared/ErrorContainer/ErrorContainer';
import { PageLoading } from '@shared/PageLoading/PageLoading';
import { pluraliseName } from '@shared/utils';
import {
  IconChartHistogram,
  IconMessage,
  IconPencil,
  IconShoppingBag,
  IconStopwatch,
  IconUsers,
} from '@tabler/icons-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { Space } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { PayWall } from './components/Paywall/PayWall';
import Gifts from './Tabs/Gifts/Gifts';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics';
import ContactMethods from './Tabs/SubscriptionDetails/ContactMethods';
import LabourDetailsView from './Tabs/SubscriptionDetails/LabourDetails';
import { ManageSubscriptions } from './Tabs/Subscriptions/ManageSubscriptions/ManageSubscriptions';
import { ShareFernLabour } from './Tabs/Subscriptions/ShareFernLabour/ShareFernLabour';
import SubscriptionRequestedModal from './Tabs/Subscriptions/SubscriptionRequestedModal/SubscriptionRequestedModal';
import { Contractions } from './Tabs/Track/Contractions';
import { FloatingContractionControls } from './Tabs/Track/FloatingContractionControls';
import { FloatingLabourUpdateControls } from './Tabs/Updates/FloatingLabourUpdateControls';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates';
import baseClasses from '@shared/shared-styles.module.css';

const FULL_ACCESS_TABS = [
  { id: 'subscriptions', label: 'Subscriptions', icon: IconUsers },
  { id: 'details', label: 'Details', icon: IconPencil },
  { id: 'updates', label: 'Updates', icon: IconMessage },
  { id: 'track', label: 'Track', icon: IconStopwatch },
  { id: 'stats', label: 'Stats', icon: IconChartHistogram },
] as const;

const SUPPORT_PERSON_TABS = [
  { id: 'subscriptions', label: 'Subscriptions', icon: IconUsers },
  { id: 'details', label: 'Details', icon: IconPencil },
  { id: 'updates', label: 'Updates', icon: IconMessage },
  { id: 'stats', label: 'Stats', icon: IconChartHistogram },
  { id: 'gifts', label: 'Gifts', icon: IconShoppingBag },
];

const LOVED_ONE_TABS = [
  { id: 'subscriptions', label: 'Subscriptions', icon: IconUsers },
  { id: 'details', label: 'Details', icon: IconPencil },
  { id: 'updates', label: 'Updates', icon: IconMessage },
  { id: 'gifts', label: 'Gifts', icon: IconShoppingBag },
] as const;

const LIMITED_TABS = [{ id: 'subscriptions', label: 'Subscriptions', icon: IconUsers }] as const;

export const SubscriberView = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { labourId, subscriberState, subscriberRole, clearSession, updateSubscription } =
    useLabourSession();
  const { isOnline } = useNetworkState();
  const promptParam = searchParams.get('prompt');
  const [modalOpened, { close: closeModal }] = useDisclosure(promptParam === 'requested');

  const getTabsForRole = () => {
    if (subscriberState !== SubscriberSessionState.Active) {
      return LIMITED_TABS;
    }
    switch (subscriberRole) {
      case SubscriberRole.BIRTH_PARTNER:
        return FULL_ACCESS_TABS;
      case SubscriberRole.SUPPORT_PERSON:
        return SUPPORT_PERSON_TABS;
      case SubscriberRole.LOVED_ONE:
      default:
        return LOVED_ONE_TABS;
    }
  };

  const TABS = getTabsForRole();
  const tabOrder = TABS.map((tab) => tab.id);

  const [activeTab, setActiveTab] = useState<string | null>('subscriptions');
  const [isUpdateControlsExpanded, setIsUpdateControlsExpanded] = useState(true);
  const [isContractionControlsExpanded, setIsContractionControlsExpanded] = useState(true);

  useEffect(() => {
    if (subscriberState !== SubscriberSessionState.Active && activeTab !== 'subscriptions') {
      setActiveTab('subscriptions');
    }
  }, [subscriberState, activeTab]);

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

  const client = useLabourV2Client();

  const shouldFetchLabour = subscriberState === SubscriberSessionState.Active && labourId !== null;
  const isBirthPartner = subscriberRole === SubscriberRole.BIRTH_PARTNER;
  const shouldFetchContractions = isBirthPartner && labourId !== null;

  const {
    isPending: isSubPending,
    isError: isSubError,
    data: subscriptionData,
    error: subError,
  } = useUserSubscriptionV2(client, shouldFetchLabour ? labourId : null);
  const {
    isPending: isLabourPending,
    isError: isLabourError,
    data: labour,
    error: labourError,
  } = useLabourByIdV2(client, shouldFetchLabour ? labourId : null);

  const { data: contractionsData } = useContractionsInfinite(
    client,
    shouldFetchContractions ? labourId : null
  );
  const contractions = useMemo(() => flattenContractions(contractionsData), [contractionsData]);

  const activeContraction = contractions.find(
    (contraction) => contraction.duration.start_time === contraction.duration.end_time
  );

  useEffect(() => {
    if (subscriptionData && shouldFetchLabour) {
      updateSubscription(subscriptionData);
    }
  }, [subscriptionData, shouldFetchLabour, updateSubscription]);

  const completed = labour?.end_time !== null;

  const scrollMainToBottom = (smooth: boolean = true) => {
    const main = document.getElementById('app-main');
    if (main) {
      main.scrollTo({ top: main.scrollHeight, behavior: smooth ? 'smooth' : 'auto' });
    }
  };

  const getFloatingControlsPadding = () => {
    if (window.innerWidth >= 768 || completed || !isBirthPartner) {
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
    return '30px';
  };

  const isPending = shouldFetchLabour && (isSubPending || isLabourPending);
  const isError = isSubError || isLabourError;
  const error = subError || labourError;

  useEffect(() => {
    if (isError && error?.message.includes('Authorization')) {
      clearSession();
      navigate('/');
    }
  }, [isError, error, clearSession, navigate]);

  if (isPending) {
    return (
      <AppShell>
        <PageLoading />
      </AppShell>
    );
  }

  if (isError && subscriberState === SubscriberSessionState.Active) {
    return (
      <AppShell>
        <ErrorContainer message={error?.message || 'An error occurred'} />
      </AppShell>
    );
  }

  const motherFirstName = labour?.mother_name?.split(' ')[0];
  const pluralisedMotherName = pluraliseName(motherFirstName || '');

  const renderTabPanel = (tabId: string) => {
    switch (tabId) {
      case 'subscriptions':
        return (
          <>
            <ManageSubscriptions />
            <Space h="xl" />
            <ShareFernLabour />
          </>
        );
      case 'details':
        if (!labour) {
          return <ErrorContainer message="Select a subscription to view details" />;
        }
        return (
          <>
            <LabourDetailsView labour={labour} birthingPersonName={pluralisedMotherName} />
            {labour.end_time == null && subscriptionData && (
              <>
                <Space h="xl" />
                {subscriptionData.access_level === 'BASIC' ? (
                  <PayWall />
                ) : (
                  <ContactMethods subscription={subscriptionData} />
                )}
              </>
            )}
          </>
        );
      case 'track':
        if (!labour) {
          return <ErrorContainer message="Select a subscription to track contractions" />;
        }
        return (
          <Contractions
            labour={labour}
            isSubscriberView
            subscriberRole={subscriberRole || undefined}
          />
        );
      case 'stats':
        if (!labour) {
          return <ErrorContainer message="Select a subscription to view statistics" />;
        }
        return <LabourStatistics labour={labour} isSubscriberView />;
      case 'updates':
        if (!labour) {
          return <ErrorContainer message="Select a subscription to view updates" />;
        }
        return (
          <LabourUpdates
            labour={labour}
            isSubscriberView
            subscriberRole={subscriberRole || undefined}
          />
        );
      case 'gifts':
        return <Gifts birthingPersonName={motherFirstName || ''} />;
      default:
        return null;
    }
  };

  return (
    <div {...swipeHandlers}>
      <AppShell navItems={TABS} activeNav={activeTab} onNavChange={setActiveTab}>
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
            {renderTabPanel(activeTab || 'subscriptions')}
          </div>
        </div>

        {isBirthPartner && labour && (
          <>
            <FloatingContractionControls
              labourCompleted={completed || false}
              activeContraction={activeContraction}
              activeTab={activeTab}
              onToggle={(expanded) => {
                setIsContractionControlsExpanded(expanded);
                if (expanded) {
                  setTimeout(() => scrollMainToBottom(true), 50);
                }
              }}
            />

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
          </>
        )}
      </AppShell>
      <SubscriptionRequestedModal opened={modalOpened} close={closeModal} />
    </div>
  );
};
