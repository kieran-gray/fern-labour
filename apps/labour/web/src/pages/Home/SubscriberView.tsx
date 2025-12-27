import { useEffect, useState } from 'react';
import { SubscriberRole } from '@base/clients/labour_service';
import { SubscriberSessionState, useLabourSession } from '@base/contexts/LabourSessionContext';
import { useLabourV2Client } from '@base/hooks';
import { useLabourByIdV2, useUserSubscriptionV2 } from '@base/hooks/useLabourData';
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
import { useNavigate } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { Center, Space } from '@mantine/core';
import { PayWall } from './components/Paywall/PayWall';
import { PendingApprovalView } from './PendingApprovalView';
import Gifts from './Tabs/Gifts/Gifts';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics';
import ContactMethods from './Tabs/SubscriptionDetails/ContactMethods';
import LabourDetailsView from './Tabs/SubscriptionDetails/LabourDetails';
import { ManageSubscriptions } from './Tabs/Subscriptions/ManageSubscriptions/ManageSubscriptions';
import { InviteContainer } from './Tabs/Subscriptions/SubscriberInviteByEmail/InviteContainer';
import { Contractions } from './Tabs/Track/Contractions';
import { LabourUpdates } from './Tabs/Updates/LabourUpdates';
import baseClasses from '@shared/shared-styles.module.css';

const BIRTH_PARTNER_TABS = [
  { id: 'subscriptions', label: 'Subscriptions', icon: IconUsers },
  { id: 'details', label: 'Details', icon: IconPencil },
  { id: 'updates', label: 'Updates', icon: IconMessage },
  { id: 'track', label: 'Track', icon: IconStopwatch },
  { id: 'stats', label: 'Stats', icon: IconChartHistogram },
] as const;

const FRIENDS_AND_FAMILY_TABS = [
  { id: 'subscriptions', label: 'Subscriptions', icon: IconUsers },
  { id: 'details', label: 'Details', icon: IconPencil },
  { id: 'updates', label: 'Updates', icon: IconMessage },
  { id: 'gifts', label: 'Gifts', icon: IconShoppingBag },
] as const;

const LIMITED_TABS = [{ id: 'subscriptions', label: 'Subscriptions', icon: IconUsers }] as const;

export const SubscriberView = () => {
  const navigate = useNavigate();
  const { labourId, subscriberState, subscriberRole, clearSubscription, clearSession } =
    useLabourSession();

  const TABS =
    subscriberState === SubscriberSessionState.Active
      ? subscriberRole === SubscriberRole.BIRTH_PARTNER
        ? BIRTH_PARTNER_TABS
        : FRIENDS_AND_FAMILY_TABS
      : LIMITED_TABS;
  const tabOrder = TABS.map((tab) => tab.id);

  const [activeTab, setActiveTab] = useState<string | null>('subscriptions');

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
        // Show pending approval view if subscription is pending
        if (subscriberState === SubscriberSessionState.PendingApproval) {
          return (
            <>
              <PendingApprovalView onCancel={clearSubscription} />
              <Space h="xl" />
              <ManageSubscriptions />
              <Space h="xl" />
              <InviteContainer />
            </>
          );
        }
        return (
          <>
            <ManageSubscriptions />
            <Space h="xl" />
            <InviteContainer />
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
        return <Contractions labour={labour} />;
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
        <div className={baseClasses.flexPageColumn}>
          <Center style={{ flexDirection: 'column' }}>
            {renderTabPanel(activeTab || 'subscriptions')}
          </Center>
        </div>
      </AppShell>
    </div>
  );
};
