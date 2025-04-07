import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Avatar, Group, Table, Text } from '@mantine/core';
import { OpenAPI, SubscriptionService } from '../../../../../../client';
import { ImportantText } from '../../../../../../shared-components/ImportantText/ImportantText';
import { PageLoadingIcon } from '../../../../../../shared-components/PageLoading/Loading';
import { useLabour } from '../../../../LabourContext';
import { ManageSubscriptionMenu } from '../ManageSubscriptionMenu/ManageSubscriptionMenu';
import classes from './SubscribersTable.module.css';

export function SubscribersTable() {
  const auth = useAuth();
  const { labourId } = useLabour();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour_subscriptions', auth.user?.profile.sub],
    queryFn: async () => {
      const response = await SubscriptionService.getLabourSubscriptions({ labourId: labourId! });
      return response;
    },
    enabled: !!labourId,
  });

  if (isPending) {
    return (
      <div style={{ display: 'flex', width: '100%', justifyContent: 'center' }}>
        <PageLoadingIcon />
      </div>
    );
  }

  if (isError) {
    return (
      <div style={{ display: 'flex', width: '100%', justifyContent: 'center' }}>
        <Text>Something went wrong... {error ? error.message : ''}</Text>
      </div>
    );
  }

  const subscriberById = Object.fromEntries(
    data.subscribers.map((subscriber) => [subscriber.id, subscriber])
  );
  const activeSubscriptions = data.subscriptions.filter(
    (subscription) => subscription.status === 'subscribed'
  );
  const rows = activeSubscriptions.map((subscription) => {
    const subscriber = subscriberById[subscription.subscriber_id];
    return (
      <Table.Tr key={subscription.id}>
        <Table.Td>
          <Group gap="sm" wrap="nowrap">
            <Avatar visibleFrom="sm" radius="xl" color="var(--mantine-color-pink-5)" />
            <div>
              <Text fz="sm" fw={500} className={classes.cropText}>
                {subscriber.first_name} {subscriber.last_name}
              </Text>
            </div>
          </Group>
        </Table.Td>
        <Table.Td>Friend/Family</Table.Td>
        <Table.Td>
          <ManageSubscriptionMenu subscription_id={subscription.id} />
        </Table.Td>
      </Table.Tr>
    );
  });

  if (rows.length > 0) {
    return (
      <Table.ScrollContainer minWidth={200} w="100%">
        <Table verticalSpacing="sm" highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Subscriber</Table.Th>
              <Table.Th>Role</Table.Th>
              <Table.Th>Manage</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </Table.ScrollContainer>
    );
  }
  return (
    <ImportantText message="You don't have any subscribers yet, share invites with loved ones in the invite tab." />
  );
}
