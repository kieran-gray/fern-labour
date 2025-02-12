import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Avatar, Group, Space, Table, Text, Title } from '@mantine/core';
import { OpenAPI, SubscriberService } from '../../../../client';
import { ErrorContainer } from '../../../../shared-components/ErrorContainer/ErrorContainer';
import { PageLoading } from '../../../../shared-components/PageLoading/PageLoading';
import { ManageSubscriberMenu } from '../ManageSubscriberMenu/ManageSubscriberMenu';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './SubscribersContainer.module.css';

export function SubscribersContainer() {
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['subscribers', auth.user?.profile.sub],
    queryFn: async () => {
      const response = await SubscriberService.getSubscribersApiV1SubscriberSubscribersGet();
      return response.subscribers;
    },
  });

  if (isPending) {
    return <PageLoading />;
  }

  if (isError) {
    return <ErrorContainer message={error.message} />;
  }

  const rows = data.map((item) => (
    <Table.Tr key={item.id} bd="none">
      <Table.Td>
        <Group gap="sm">
          <Avatar radius="xl" color="var(--mantine-color-pink-5)" />
          <div>
            <Text fz="sm" fw={500}>
              {item.first_name} {item.last_name}
            </Text>
            <Text fz="xs" c="var(--mantine-color-gray-7)">
              {item.email}
            </Text>
          </div>
        </Group>
      </Table.Td>
      <Table.Td>Friend/Family</Table.Td>
      <Table.Td>
        <ManageSubscriberMenu subscriber_id={item.id} />
      </Table.Td>
    </Table.Tr>
  ));

  if (rows.length > 0) {
    return (
      <>
        <div className={baseClasses.root} style={{ maxWidth: '1100px' }}>
          <div className={baseClasses.header}>
            <Title fz="xl" className={baseClasses.title}>
              Your Subscribers
            </Title>
          </div>
          <div className={baseClasses.body}>
            <div className={classes.inner}>
              <div className={baseClasses.flexRow}>
                <div className={baseClasses.flexColumn} style={{ width: '100%' }}>
                  <Title className={classes.title}>Manage your subscribers</Title>
                  <Text c="var(--mantine-color-gray-7)" mt="md">
                    Here, you can view and manage the subscribers following your labour journey.
                    <br />
                    Update their roles and remove or block them if needed.
                    <br />
                    Stay in control of who can stay connected and support you during this special
                    time.
                    <br />
                  </Text>
                </div>
                <div className={baseClasses.flexColumn} style={{ flexGrow: 1 }}>
                  <Table.ScrollContainer minWidth={200}>
                    <Table verticalSpacing="sm">
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
                </div>
              </div>
            </div>
          </div>
        </div>
        <Space h="xl" />
      </>
    );
  }
}
