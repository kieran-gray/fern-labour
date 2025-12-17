import { useState } from 'react';
import { useLabourSession } from '@base/contexts';
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
  IconUsers,
} from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { Center, Space } from '@mantine/core';
import { InviteContainer } from '../Subscriptions/Components/InviteContainer/InviteContainer';
import { SubscriptionsContainer } from '../Subscriptions/Components/ManageSubscriptions/ManageSubscriptions';
import { PayWall } from './Paywall/PayWall';
import Gifts from './Tabs/Gifts/Gifts';
import ContactMethods from './Tabs/LabourDetails/ContactMethods';
import LabourDetails from './Tabs/LabourDetails/LabourDetails';
import { StatusUpdates } from './Tabs/LabourUpdates/LabourUpdates';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics';
import baseClasses from '@shared/shared-styles.module.css';

const TABS = [
  { id: 'subscriptions', label: 'Subscriptions', icon: IconUsers },
  { id: 'details', label: 'Details', icon: IconPencil },
  { id: 'updates', label: 'Updates', icon: IconMessage },
  { id: 'stats', label: 'Stats', icon: IconChartHistogram },
  { id: 'gifts', label: 'Gifts', icon: IconShoppingBag },
] as const;

const tabOrder = TABS.map((tab) => tab.id);

export const SubscriptionPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<string | null>('details');

  const { labourId, subscriptionId, setSubscriptionId } = useLabourSession();

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
    trackTouch: true,
    preventScrollOnSwipe: true,
  });

  const client = useLabourV2Client();
  const { isPending, isError, data, error } = useUserSubscriptionV2(client, labourId);
  const {
    isPending: isLabourPending,
    isError: isLabourError,
    data: labour,
    error: labourError,
  } = useLabourByIdV2(client, labourId);

  if (isPending || isLabourPending) {
    return (
      <AppShell>
        <PageLoading />
      </AppShell>
    );
  }

  if (isError || isLabourError) {
    if (error?.message.includes('not found') || labourError?.message.includes('not found')) {
      setSubscriptionId('');
      navigate('/');
    }
    return (
      <AppShell>
        <ErrorContainer message={error?.message || labourError?.message || ''} />
      </AppShell>
    );
  }

  const motherFirstName = labour?.mother_name.split(' ')[0];
  const pluralisedMotherName = pluraliseName(motherFirstName || '');

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
            <LabourDetails labour={labour} birthingPersonName={pluralisedMotherName} />
            {labour.end_time == null && (
              <>
                <Space h="xl" />
                {(data.access_level === 'BASIC' && <PayWall />) || (
                  <ContactMethods subscription={data} />
                )}
              </>
            )}
          </>
        );
      case 'stats':
        return <LabourStatistics labour={labour} />;
      case 'updates':
        return <StatusUpdates labour={labour} />;
      case 'gifts':
        return <Gifts birthingPersonName={motherFirstName} />;
      default:
        return null;
    }
  };

  return (
    <div {...swipeHandlers}>
      <AppShell navItems={TABS} activeNav={activeTab} onNavChange={setActiveTab}>
        {/* Content Area */}
        <div className={baseClasses.flexPageColumn}>
          <Center style={{ flexDirection: 'column' }}>
            {renderTabPanel(activeTab || 'details')}
          </Center>
        </div>
      </AppShell>
    </div>
  );
};
