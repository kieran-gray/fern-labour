
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Avatar, Group, Table, Text } from '@mantine/core';
import { OpenAPI, SubscriberService } from '../../../../client';
import { ErrorContainer } from '../../../../shared-components/ErrorContainer/ErrorContainer';
import { PageLoading } from '../../../../shared-components/PageLoading/PageLoading';
import { ManageSubscriberMenu } from '../ManageSubscriberMenu/ManageSubscriberMenu';
import classes from './SubscribersTable.module.css';

export function SubscribersTable() {
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
            <Group gap="sm" wrap='nowrap'>
                <Avatar radius="xl" color="var(--mantine-color-pink-5)" />
                <div>
                <Text fz="sm" fw={500} className={classes.cropText}>
                    {item.first_name} {item.last_name}
                </Text>
                <Text fz="xs" c="var(--mantine-color-gray-7)" className={classes.cropText}>
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
            <Table.ScrollContainer minWidth={200} w='100%'>
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
        )
    }
    return (<Text>You don't have any subscribers yet, invite them below</Text>)
}