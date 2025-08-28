import { useLabour } from '@labour/LabourContext';
import { useLabourHistory } from '@shared/hooks';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { PageLoadingIcon } from '@shared/PageLoading/Loading';
import { IconArrowRight, IconInfoCircle, IconX } from '@tabler/icons-react';
import { useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Badge, Button, Table, Text } from '@mantine/core';
import { ManageLabourMenu } from '../ManageLabourMenu/ManageLabourMenu';
import classes from './LabourHistoryTable.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function LabourHistoryTable() {
  const { labourId, setLabourId } = useLabour();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { isPending, isError, data, error } = useLabourHistory();

  const labours = data?.labours || [];

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

  const sortedLabours = labours.sort((a, b) =>
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

  const toggleButtonIcon = (clickedLabourId: string) => {
    return labourId === clickedLabourId ? (
      <IconX size={18} stroke={1.5} />
    ) : (
      <IconArrowRight size={18} stroke={1.5} />
    );
  };

  const rows = sortedLabours.map((labour) => {
    const date =
      labour.end_time != null
        ? new Date(labour.end_time).toISOString().substring(0, 10)
        : new Date(labour.due_date).toISOString().substring(0, 10);
    return (
      <Table.Tr key={labour.id}>
        <Table.Td>
          <div
            className={baseClasses.flexRow}
            style={{ alignItems: 'center', justifyContent: 'space-around', rowGap: '5px' }}
          >
            <Badge variant="light" size="lg" visibleFrom="xs">
              <Text fz="md" fw={700} className={classes.cropText}>
                {labour.current_phase}
              </Text>
            </Badge>
            <Badge variant="light" size="xs" hiddenFrom="xs">
              <Text fz="xs" fw={700} className={classes.cropText}>
                {labour.current_phase}
              </Text>
            </Badge>
            <Text fz="md" fw={500} ta="center" visibleFrom="xs">
              {labour.labour_name || date}
            </Text>
            <Text fz="xs" fw={500} ta="center" hiddenFrom="xs">
              {labour.labour_name || date}
            </Text>
          </div>
        </Table.Td>
        <Table.Td>
          <Button
            color="var(--mantine-primary-color-4)"
            rightSection={toggleButtonIcon(labour.id)}
            variant="light"
            radius="xl"
            size="md"
            visibleFrom="xs"
            className={classes.submitButton}
            onClick={() => setLabour(labour.id)}
            type="submit"
          >
            {labourId === labour.id ? 'Exit' : 'View'}
          </Button>
          <Button
            color="var(--mantine-primary-color-4)"
            rightSection={toggleButtonIcon(labour.id)}
            variant="light"
            radius="xl"
            size="xs"
            hiddenFrom="xs"
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
        <Table verticalSpacing="sm" highlightOnHover ta="center">
          <Table.Thead>
            <Table.Tr>
              <Table.Th ta="center">Labour</Table.Th>
              <Table.Th ta="center">View</Table.Th>
              <Table.Th ta="center">Manage</Table.Th>
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
