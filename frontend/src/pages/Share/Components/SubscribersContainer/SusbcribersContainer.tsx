import { Button, Group, Table, Text, Title } from '@mantine/core';
import baseClasses from '../../../../shared-components/shared-styles.module.css'
import { useAuth } from 'react-oidc-context';
import { SubscriberService, OpenAPI } from '../../../../client';
import { useQuery } from '@tanstack/react-query';
import { ErrorContainer } from '../../../../shared-components/ErrorContainer/ErrorContainer';
import { PageLoading } from '../../../../shared-components/PageLoading/PageLoading';
import { IconCircleMinus } from '@tabler/icons-react';
import { notifications } from '@mantine/notifications';

export function SubscribersContainer() {
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || ""
  }

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['subscribers', auth.user?.profile.sub],
    queryFn: async () => {
      const response = await SubscriberService.getSubscribersApiV1SubscriberSubscribersGet()
      return response.subscribers;
    }
  });

  if (isPending) {
    return (
        <PageLoading />
    );
  }

  if (isError) {
    return (
        <ErrorContainer message={error.message} />
    );
  }
  
  const removeSubscriber = () => {
    notifications.show(
        {
            title: 'Error',
            message: "Not implemented",
            radius: "lg",
            color: "var(--mantine-color-pink-9)",
            classNames: {
                title: baseClasses.notificationTitle,
                description: baseClasses.notificationDescription
            },
            style:{ backgroundColor: "var(--mantine-color-pink-4)", color: "var(--mantine-color-white)" }
        }
    );
}

  const rows = data.map((item) => (
    <Table.Tr key={item.id}>
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
      <Table.Td>
        <Button
            color='var(--mantine-color-pink-4)'
            variant="filled"
            rightSection={
            <IconCircleMinus size={20} stroke={1.5} />
            }
            radius="xl"
            size="md"
            pr={14}
            h={32}
            styles={{ section: { marginLeft: 22 } }}
            type="submit"
            onClick={removeSubscriber}
        >
            Remove
        </Button>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <div className={baseClasses.root}>
    <div className={baseClasses.header}>
      <Title fz="xl" className={baseClasses.title}>Your Subscribers</Title>
    </div>
    <div className={baseClasses.body}>
    <Table.ScrollContainer minWidth={200}>
        <Table verticalSpacing="sm">
        <Table.Thead>
            <Table.Tr>
            <Table.Th>Subscriber</Table.Th>
            <Table.Th>Remove</Table.Th>
            </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
        </Table>
    </Table.ScrollContainer>
    </div>
  </div>
  )
}

