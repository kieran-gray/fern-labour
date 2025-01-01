import { Avatar, Badge, Group, Table, Text } from '@mantine/core';
import { BirthingPersonSummaryDTO } from '../../client';


export function SubscriptionsTable({subscriptions}: {subscriptions: BirthingPersonSummaryDTO[]}) {
  const rows = subscriptions.map((subscription) => (
    <Table.Tr key={subscription.id}>
      <Table.Td>
        <Group gap="sm">
          <Avatar size={40} radius={40} />
          <div>
            <Text fz="sm" fw={500}>
              {subscription.first_name} {subscription.last_name}
            </Text>
          </div>
        </Group>
      </Table.Td>
      <Table.Td>
        {subscription.active_labour ? (
          <Badge fullWidth variant="light">
            In Labour
          </Badge>
        ) : (
          <Badge color="gray" fullWidth variant="light">
            Not In Labour
          </Badge>
        )}
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Table.ScrollContainer minWidth={800}>
      <Table verticalSpacing="sm">
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th>
            <Table.Th>Active Labour</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Table.ScrollContainer>
  );
}