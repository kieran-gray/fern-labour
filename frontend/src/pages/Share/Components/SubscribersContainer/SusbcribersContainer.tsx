import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Group, Space, Table, Text, Title } from '@mantine/core';
import { OpenAPI, SubscriberService } from '../../../../client';
import { ErrorContainer } from '../../../../shared-components/ErrorContainer/ErrorContainer';
import { PageLoading } from '../../../../shared-components/PageLoading/PageLoading';
import { RemoveSubscriberButton } from '../RemoveSubscriberButton/RemoveSubscriberButton';
import baseClasses from '../../../../shared-components/shared-styles.module.css';

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
          <div>
            <Text fz="sm" fw={500}>
              {item.first_name} {item.last_name}
            </Text>
            <Text fz="xs" c="dimmed">
              {item.email}
            </Text>
          </div>
        </Group>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <RemoveSubscriberButton subscriber_id={item.id} />
      </Table.Td>
    </Table.Tr>
  ));

  if (rows.length > 0) {
    return (
      <>
        <div className={baseClasses.root}>
          <div className={baseClasses.header}>
            <Title fz="xl" className={baseClasses.title}>
              Your Subscribers
            </Title>
          </div>
          <div className={baseClasses.body}>
            <Table.ScrollContainer minWidth={200}>
              <Table verticalSpacing="sm">
                <Table.Tbody>{rows}</Table.Tbody>
              </Table>
            </Table.ScrollContainer>
          </div>
        </div>
        <Space h="xl" />
      </>
    );
  }
}
