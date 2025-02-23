import {
  IconChartHistogram,
  IconMessage,
  IconPencil,
  IconSpeakerphone,
  IconUsers,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Space, Tabs, Text } from '@mantine/core';
import { OpenAPI, SubscriptionService } from '../../client/index.ts';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { pluraliseName } from '../../shared-components/utils.tsx';
import { InviteContainer } from '../Subscriptions/Components/InviteContainer/InviteContainer.tsx';
import { SubscriptionsContainer } from '../Subscriptions/Components/ManageSubscriptions/ManageSubscriptions.tsx';
import { useSubscription } from './SubscriptionContext.tsx';
import { Announcements } from './Tabs/Announcements/Announcements.tsx';
import ContactMethodsForm from './Tabs/LabourDetails/ContactMethodsForm.tsx';
import LabourDetails from './Tabs/LabourDetails/LabourDetails.tsx';
import { LabourStatistics } from './Tabs/Statistics/LabourStatistics.tsx';
import { StatusUpdates } from './Tabs/StatusUpdates/StatusUpdates.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const SubscriptionPage = () => {
  const auth = useAuth();
  const { subscriptionId } = useSubscription();

  if (!subscriptionId) {
    throw new Error('subscriptionId is required');
  }

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['subscription_data', subscriptionId, auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response =
          await SubscriptionService.getSubscriptionByIdApiV1SubscriptionSubscriptionDataSubscriptionIdGet(
            {
              subscriptionId,
            }
          );
        return response;
      } catch (err) {
        throw new Error('Failed to load subscription. Please try again later.');
      }
    },
  });

  if (isPending) {
    return (
      <AppShell>
        <PageLoading />
      </AppShell>
    );
  }

  if (isError) {
    return (
      <AppShell>
        <ErrorContainer message={error.message} />
      </AppShell>
    );
  }

  const pluralisedBirthingPersonName = pluraliseName(data.birthing_person.first_name);

  return (
    <AppShell>
      <Tabs
        w="100%"
        defaultValue="details"
        radius="lg"
        classNames={{
          list: baseClasses.navTabs,
          tab: baseClasses.navTab,
          tabSection: baseClasses.navTabSection,
        }}
      >
        <Tabs.List grow>
          <Tabs.Tab value="subscriptions" leftSection={<IconUsers />}>
            <Text className={baseClasses.navTabText}>Subscriptions</Text>
          </Tabs.Tab>
          <Tabs.Tab value="updates" leftSection={<IconMessage />}>
            <Text className={baseClasses.navTabText}>Updates</Text>
          </Tabs.Tab>
          <Tabs.Tab value="details" leftSection={<IconPencil />}>
            <Text className={baseClasses.navTabText}>Details</Text>
          </Tabs.Tab>
          <Tabs.Tab value="announcements" leftSection={<IconSpeakerphone />}>
            <Text className={baseClasses.navTabText}>Announcements</Text>
          </Tabs.Tab>
          <Tabs.Tab value="stats" leftSection={<IconChartHistogram />}>
            <Text className={baseClasses.navTabText}>Stats</Text>
          </Tabs.Tab>
        </Tabs.List>
        <div className={baseClasses.flexPageColumn}>
          <Tabs.Panel value="subscriptions">
            <Space h="xl" />
            <SubscriptionsContainer />
            <Space h="xl" />
            <InviteContainer />
          </Tabs.Panel>
          <Tabs.Panel value="details">
            <Space h="xl" />
            <LabourDetails labour={data.labour} birthingPersonName={pluralisedBirthingPersonName} />
            <Space h="xl" />
            <ContactMethodsForm subscription={data.subscription} />
          </Tabs.Panel>
          <Tabs.Panel value="stats" keepMounted={false}>
            <Space h="xl" />
            <LabourStatistics
              labour={data.labour}
              birthingPersonName={pluralisedBirthingPersonName}
            />
          </Tabs.Panel>
          <Tabs.Panel value="updates">
            <Space h="xl" />
            <StatusUpdates labour={data.labour} birthingPerson={data.birthing_person} />
          </Tabs.Panel>
          <Tabs.Panel value="announcements">
            <Space h="xl" />
            <Announcements labour={data.labour} birthingPersonName={pluralisedBirthingPersonName} />
          </Tabs.Panel>
        </div>
      </Tabs>
    </AppShell>
  );
};
