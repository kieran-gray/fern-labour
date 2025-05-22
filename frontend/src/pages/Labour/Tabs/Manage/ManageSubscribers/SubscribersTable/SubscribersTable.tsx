import { Avatar, Group, Table, Text } from '@mantine/core';
import { SubscriptionDTO, UserSummaryDTO } from '../../../../../../clients/labour_service';
import { ManageSubscriptionMenu } from '../ManageSubscriptionMenu/ManageSubscriptionMenu';
import baseClasses from '../../../../../../shared-components/shared-styles.module.css';
import classes from './SubscribersTable.module.css';

export function SubscribersTable({
  subscriptions,
  subscriberById,
  status,
}: {
  subscriptions: SubscriptionDTO[];
  subscriberById: { [k: string]: UserSummaryDTO };
  status: string;
}) {
  const rows = subscriptions.map((subscription) => {
    const subscriber = subscriberById[subscription.subscriber_id];
    return (
      <Table.Tr key={subscription.id}>
        <Table.Td>
          <Group gap="sm" wrap="nowrap">
            <Avatar visibleFrom="sm" radius="xl" color="var(--mantine-color-pink-5)" />
            <>
              <Text fz="sm" visibleFrom="xs" fw={500} className={classes.cropText}>
                {subscriber.first_name} {subscriber.last_name}
              </Text>
              <Text fz="xs" hiddenFrom="xs" fw={500} className={classes.cropText}>
                {subscriber.first_name} {subscriber.last_name}
              </Text>
            </>
          </Group>
        </Table.Td>
        <Table.Td>
          <>
            <Text fz="sm" visibleFrom="xs" fw={500} className={classes.cropText}>
              {subscription.status}
            </Text>
            <Text fz="xs" hiddenFrom="xs" fw={500} className={classes.cropText}>
              {subscription.status}
            </Text>
          </>
        </Table.Td>
        <Table.Td>
          <ManageSubscriptionMenu subscription_id={subscription.id} status={status} />
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
              <Table.Th>Status</Table.Th>
              <Table.Th>Manage</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </Table.ScrollContainer>
    );
  }
  let message = undefined;
  if (status === 'subscribed') {
    message =
      "You don't have any subscribers yet, share invites with loved ones in the invite tab.";
  } else if (status === 'requested') {
    message = "You don't have any subscriber requests.";
  } else if (status === 'blocked') {
    message = "You don't have any blocked subscribers.";
  }

  return (
    <>
      <Text
        className={baseClasses.importantText}
        bg="var(--mantine-color-pink-0)"
        size="sm"
        hiddenFrom="sm"
        mt={10}
      >
        {message}
      </Text>
      <Text
        className={baseClasses.importantText}
        bg="var(--mantine-color-pink-0)"
        size="md"
        visibleFrom="sm"
        mt={10}
      >
        {message}
      </Text>
    </>
  );
}
