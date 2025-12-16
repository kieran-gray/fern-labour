import { useState } from 'react';
import { useSubscription } from '@base/contexts/SubscriptionContext';
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
import { useUserSubscriptionV2 } from '@base/shared-components/hooks/v2/useLabourDataV2';
import { useLabourV2Client } from '@base/shared-components/hooks';

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
  const { subscriptionId, setSubscriptionId } = useSubscription();
  const [activeTab, setActiveTab] = useState<string | null>('details');

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
  const { isPending, isError, data, error } = useUserSubscriptionV2(subscriptionId);

  if (isPending) {
    return (
      <AppShell>
        <PageLoading />
      </AppShell>
    );
  }

  if (isError) {
    if (error.message.includes('not found')) {
      setSubscriptionId('');
      navigate('/');
    }
    return (
      <AppShell>
        <ErrorContainer message={error.message} />
      </AppShell>
    );
  }

  const pluralisedBirthingPersonName = pluraliseName(data.birthing_person.first_name);

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
            <LabourDetails labour={data.labour} birthingPersonName={pluralisedBirthingPersonName} />
            {data.labour.end_time == null && (
              <>
                <Space h="xl" />
                {(data.subscription.access_level === 'basic' && <PayWall />) || (
                  <ContactMethods subscription={data.subscription} />
                )}
              </>
            )}
          </>
        );
      case 'stats':
        return (
          <LabourStatistics
            labour={data.labour}
            birthingPersonName={pluralisedBirthingPersonName}
          />
        );
      case 'updates':
        return <StatusUpdates labour={data.labour} birthingPerson={data.birthing_person} />;
      case 'gifts':
        return <Gifts birthingPersonName={data.birthing_person.first_name} />;
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
