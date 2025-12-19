import { ReactElement } from 'react';
import { SubscriptionStatusReadModel } from '@base/clients/labour_service/types';
import { useLabourSession } from '@base/contexts';
import { useLabourV2Client } from '@base/hooks';
import { useUserSubscribedLaboursV2, useUserSubscriptionsV2 } from '@base/hooks/useLabourData';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { PageLoadingIcon } from '@shared/PageLoading/Loading';
import { IconArrowRight, IconX } from '@tabler/icons-react';
import { Avatar, Button, Group, Table, Text } from '@mantine/core';
import { ManageSubscriptionMenu } from '../ManageSubscriptionMenu/ManageSubscriptionMenu';
import classes from './SubscriptionsTable.module.css';

export function SubscriptionsTable() {
  const { subscriptionId, setSubscriptionId, setLabourId } = useLabourSession();

  const client = useLabourV2Client();
  const { isPending, isError, data, error } = useUserSubscriptionsV2(client);
  const { data: labours, isPending: laboursLoading } = useUserSubscribedLaboursV2(client);

  if (isPending || laboursLoading) {
    return (
      <div style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
        <PageLoadingIcon />
      </div>
    );
  }

  if (isError) {
    return <ImportantText message={error.message} />;
  }

  const toggleSubscription = (subscription: SubscriptionStatusReadModel) => {
    if (subscriptionId === subscription.subscription_id) {
      setSubscriptionId(null);
    } else {
      setSubscriptionId(subscription.subscription_id);
      setLabourId(subscription.labour_id);
    }
  };
  const toggleButtonIcon = (subId: string) => {
    return subscriptionId === subId ? (
      <IconX size={18} stroke={1.5} />
    ) : (
      <IconArrowRight size={18} stroke={1.5} />
    );
  };

  const rows: ReactElement[] = [];

  data.forEach((subscription) => {
    if (subscription.status !== 'SUBSCRIBED') {
      return
    }
    
    const labour = labours?.find((l) => l.labour_id === subscription.labour_id);
    const motherName = labour?.mother_name || 'Unknown';

    rows.push(
      <Table.Tr key={subscription.subscription_id}>
        <Table.Td>
          <Group gap="sm" wrap="nowrap">
            <Avatar visibleFrom="sm" radius="xl" color="var(--mantine-primary-color-5)" />
            <>
              <Text fw={500} className={classes.cropText} size="xs" hiddenFrom="xs">
                {motherName}
              </Text>
              <Text fw={500} className={classes.cropText} size="sm" visibleFrom="xs">
                {motherName}
              </Text>
            </>
          </Group>
        </Table.Td>
        <Table.Td>
          <Button
            color="var(--mantine-primary-color-4)"
            rightSection={toggleButtonIcon(subscription.subscription_id)}
            variant="light"
            radius="xl"
            size="md"
            visibleFrom="sm"
            className={classes.submitButton}
            onClick={() => toggleSubscription(subscription)}
            type="submit"
          >
            {subscriptionId === subscription.subscription_id ? 'Exit' : 'View'}
          </Button>
          <Button
            color="var(--mantine-primary-color-4)"
            rightSection={toggleButtonIcon(subscription.subscription_id)}
            variant="light"
            radius="xl"
            size="xs"
            h={40}
            hiddenFrom="sm"
            className={classes.submitButton}
            onClick={() => toggleSubscription(subscription)}
            type="submit"
          >
            {subscriptionId === subscription.subscription_id ? 'Exit' : 'View'}
          </Button>
        </Table.Td>
        <Table.Td>
          <ManageSubscriptionMenu labourId={subscription.labour_id} subscriptionId={subscription.subscription_id} />
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
              <Table.Th>Mother</Table.Th>
              <Table.Th>Labour</Table.Th>
              <Table.Th>Manage</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </Table.ScrollContainer>
    );
  }
  return <ImportantText message="You don't have any subscriptions yet." />;
}
