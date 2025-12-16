import { ReactElement } from 'react';
import { useSubscription } from '@base/contexts/SubscriptionContext';
import { useLabourV2Client } from '@shared/hooks';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { PageLoadingIcon } from '@shared/PageLoading/Loading';
import { IconArrowRight, IconX } from '@tabler/icons-react';
import { Button, Table } from '@mantine/core';
import { ManageSubscriptionMenu } from '../ManageSubscriptionMenu/ManageSubscriptionMenu';
import classes from './SubscriptionsTable.module.css';
import { useUserSubscriptionsV2 } from '@base/shared-components/hooks/v2/useLabourDataV2';

export function SubscriptionsTable() {
  const { subscriptionId, setSubscriptionId } = useSubscription();

  const client = useLabourV2Client();
  const { isPending, isError, data, error } = useUserSubscriptionsV2(client);

  if (isPending) {
    return (
      <div style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
        <PageLoadingIcon />
      </div>
    );
  }

  if (isError) {
    return <ImportantText message={error.message} />;
  }

  const toggleSubscription = (subId: string) => {
    subscriptionId === subId ? setSubscriptionId('') : setSubscriptionId(subId);
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
    rows.push(
      <Table.Tr key={subscription.subscription_id}>
        <Table.Td>
          <Button
            color="var(--mantine-primary-color-4)"
            rightSection={toggleButtonIcon(subscription.subscription_id)}
            variant="light"
            radius="xl"
            size="md"
            visibleFrom="sm"
            className={classes.submitButton}
            onClick={() => toggleSubscription(subscription.subscription_id)}
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
            onClick={() => toggleSubscription(subscription.subscription_id)}
            type="submit"
          >
            {subscriptionId === subscription.subscription_id ? 'Exit' : 'View'}
          </Button>
        </Table.Td>
        <Table.Td>
          <ManageSubscriptionMenu labour_id={subscription.labour_id} />
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
