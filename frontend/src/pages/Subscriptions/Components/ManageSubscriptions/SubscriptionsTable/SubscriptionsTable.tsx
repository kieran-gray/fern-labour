import { IconArrowRight, IconInfoCircle, IconX } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Avatar, Button, Group, Table, Text } from '@mantine/core';
import { OpenAPI, SubscriptionService } from '../../../../../client';
import { ImportantText } from '../../../../../shared-components/ImportantText/ImportantText';
import { PageLoadingIcon } from '../../../../../shared-components/PageLoading/Loading';
import { useSubscription } from '../../../../Subscription/SubscriptionContext';
import { ManageSubscriptionMenu } from '../ManageSubscriptionMenu/ManageSubscriptionMenu';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
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
        const response =
          await SubscriptionService.getSubscriberSubscriptionsApiV1SubscriptionSubscriberSubscriptionsGet();
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

  const birthingPersons = data.birthing_persons || [];

  const birthingPersonById = Object.fromEntries(
    birthingPersons.map((birthingPerson) => [birthingPerson.id, birthingPerson])
  );
  const rows = data.subscriptions.map((subscription) => {
    const birthing_person = birthingPersonById[subscription.birthing_person_id];
    return (
      <Table.Tr key={subscription.id} bd="none">
        <Table.Td>
          <Group gap="sm" wrap="nowrap">
            <Avatar radius="xl" color="var(--mantine-color-pink-5)" />
            <div>
              <Text fz="sm" fw={500} className={classes.cropText}>
                {birthing_person.first_name} {birthing_person.last_name}
              </Text>
            </div>
          </Group>
        </Table.Td>
        <Table.Td>
          <Button
            color="var(--mantine-color-pink-4)"
            rightSection={
              subscriptionId === subscription.id ? (
                <IconX size={18} stroke={1.5} />
              ) : (
                <IconArrowRight size={18} stroke={1.5} />
              )
            }
            variant="light"
            radius="xl"
            size="sm"
            h={48}
            className={classes.submitButton}
            onClick={() => {
              subscriptionId === subscription.id
                ? setSubscriptionId('')
                : setSubscriptionId(subscription.id);
            }}
            type="submit"
          >
            {subscriptionId === subscription.id ? 'Exit Labour' : 'View Labour'}
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
  return (
    <Text className={baseClasses.importantText}>
      <IconInfoCircle
        size={20}
        style={{ alignSelf: 'center', marginRight: '10px', flexShrink: 0 }}
      />
      You don't have any subscriptions yet.{' '}
    </Text>
  );
}
