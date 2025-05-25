import { ReactElement } from 'react';
import { OpenAPI, SubscriptionService } from '@clients/labour_service';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { PageLoadingIcon } from '@shared/PageLoading/Loading';
import { useSubscription } from '@subscription/SubscriptionContext';
import { IconArrowRight, IconX } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Avatar, Button, Group, Table, Text } from '@mantine/core';
import { ManageSubscriptionMenu } from '../ManageSubscriptionMenu/ManageSubscriptionMenu';
import classes from './SubscriptionsTable.module.css';

export function SubscriptionsTable() {
  const auth = useAuth();
  const { subscriptionId, setSubscriptionId } = useSubscription();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['subscriber_subscriptions', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await SubscriptionService.getSubscriberSubscriptions();
        return response;
      } catch (err) {
        throw new Error('Failed to load subscriptions. Please try again later.');
      }
    },
  });

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

  const birthingPersons = data.birthing_persons || [];

  const birthingPersonById = Object.fromEntries(
    birthingPersons.map((birthingPerson) => [birthingPerson.id, birthingPerson])
  );
  const rows: ReactElement[] = [];

  data.subscriptions.forEach((subscription) => {
    const birthing_person = birthingPersonById[subscription.birthing_person_id];
    if (!birthing_person) {
      return;
    }
    rows.push(
      <Table.Tr key={subscription.id}>
        <Table.Td>
          <Group gap="sm" wrap="nowrap">
            <Avatar visibleFrom="sm" radius="xl" color="var(--mantine-primary-color-5)" />
            <>
              <Text fw={500} className={classes.cropText} size="xs" hiddenFrom="xs">
                {birthing_person.first_name} {birthing_person.last_name}
              </Text>
              <Text fw={500} className={classes.cropText} size="sm" visibleFrom="xs">
                {birthing_person.first_name} {birthing_person.last_name}
              </Text>
            </>
          </Group>
        </Table.Td>
        <Table.Td>
          <Button
            color="var(--mantine-primary-color-4)"
            rightSection={toggleButtonIcon(subscription.id)}
            variant="light"
            radius="xl"
            size="md"
            visibleFrom="sm"
            className={classes.submitButton}
            onClick={() => toggleSubscription(subscription.id)}
            type="submit"
          >
            {subscriptionId === subscription.id ? 'Exit' : 'View'}
          </Button>
          <Button
            color="var(--mantine-primary-color-4)"
            rightSection={toggleButtonIcon(subscription.id)}
            variant="light"
            radius="xl"
            size="xs"
            h={40}
            hiddenFrom="sm"
            className={classes.submitButton}
            onClick={() => toggleSubscription(subscription.id)}
            type="submit"
          >
            {subscriptionId === subscription.id ? 'Exit' : 'View'}
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
