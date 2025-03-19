import { IconArrowRight, IconInfoCircle, IconX } from '@tabler/icons-react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Badge, Button, Group, Table, Text } from '@mantine/core';
import { LabourService, OpenAPI } from '../../../../../client';
import { ImportantText } from '../../../../../shared-components/ImportantText/ImportantText';
import { PageLoadingIcon } from '../../../../../shared-components/PageLoading/Loading';
import { useLabour } from '../../../../Labour/LabourContext';
import { ManageLabourMenu } from '../ManageLabourMenu/ManageLabourMenu';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './LabourHistoryTable.module.css';

export function LabourHistoryTable() {
  const auth = useAuth();
  const { labourId, setLabourId } = useLabour();
  const navigate = useNavigate();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labours', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getAllLaboursApiV1LabourGetAllGet();
        return response.labours;
      } catch (err) {
        throw new Error('Failed to load labours. Please try again later.');
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

  const sortedLabours = data.sort((a, b) =>
    a.due_date < b.due_date ? -1 : a.due_date > b.due_date ? 1 : 0
  );

  const setLabour = async (newLabourId: string) => {
    await queryClient.invalidateQueries();
    if (labourId === newLabourId) {
      setLabourId(null);
    } else {
      setLabourId(newLabourId);
      navigate(`/?labourId=${newLabourId}`);
    }
  };

  const rows = sortedLabours.map((labour) => {
    const date =
      labour.end_time != null
        ? new Date(labour.end_time).toDateString()
        : new Date(labour.due_date).toDateString();
    return (
      <Table.Tr key={labour.id} bd="none">
        <Table.Td>
          <Text fz="sm" fw={500} className={classes.cropText}>
            {labour.labour_name || date}
          </Text>
        </Table.Td>
        <Table.Td>
          <Group gap="sm" wrap="nowrap">
            <Badge variant="light" className={classes.labourBadge} size="sm">
              <Text fz="sm" fw={700} className={classes.cropText}>
                {labour.current_phase}
              </Text>
            </Badge>
          </Group>
        </Table.Td>
        <Table.Td>
          <Button
            color="var(--mantine-color-pink-4)"
            rightSection={
              labourId === labour.id ? (
                <IconX size={18} stroke={1.5} />
              ) : (
                <IconArrowRight size={18} stroke={1.5} />
              )
            }
            variant="light"
            radius="xl"
            size="sm"
            className={classes.submitButton}
            onClick={() => setLabour(labour.id)}
            type="submit"
          >
            {labourId === labour.id ? 'Exit' : 'View'}
          </Button>
        </Table.Td>
        <Table.Td>
          <ManageLabourMenu labourId={labour.id} />
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
              <Table.Th>Labour</Table.Th>
              <Table.Th>Status</Table.Th>
              <Table.Th>View</Table.Th>
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
      You don't have any labours yet.{' '}
    </Text>
  );
}
