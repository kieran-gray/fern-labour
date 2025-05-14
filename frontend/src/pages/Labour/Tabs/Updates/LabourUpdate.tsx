import { Badge, Group, LoadingOverlay, Text } from '@mantine/core';
import { LabourUpdateDTO } from '../../../../clients/labour_service';
import { ManageLabourUpdateMenu } from './ManageLabourUpdateMenu';
import classes from './LabourUpdates.module.css';

export function LabourUpdate({
  data,
  completed,
  owner,
}: {
  data: LabourUpdateDTO;
  completed: boolean;
  owner: boolean;
}) {
  const announce = data.labour_update_type === 'announcement';
  return (
    <div className={announce ? classes.announcementPanel : classes.statusUpdatePanel} id={data.id}>
      <LoadingOverlay visible={data.id === 'placeholder'} />
      <Group>
        <Text>{(announce && '📣') || '💫'}</Text>
        <Badge
          visibleFrom="xs"
          variant="filled"
          size="md"
          radius="md"
          bg={(announce && 'var(--mantine-color-pink-6)') || '#24968b'}
        >
          {data.labour_update_type.split('_')[0]}
        </Badge>
        <Badge
          hiddenFrom="xs"
          variant="filled"
          size="sm"
          radius="md"
          bg={(announce && 'var(--mantine-color-pink-6)') || '#24968b'}
        >
          {data.labour_update_type.split('_')[0]}
        </Badge>

        <div style={{ flexGrow: 1 }} />
        <Text size="xs" c="var(--mantine-color-gray-9)">
          {new Date(data.sent_time).toLocaleString().slice(0, 17).replace(',', ' at')}
        </Text>
      </Group>
      <Text pt="sm" size="md" fw="400">
        {data.message}
      </Text>
      {owner && (
        <div className={classes.messageFooter}>
          <Text size="xs">
            {(announce && '📡 Broadcast to subscribers') || '👁️ Visible to subscribers'}
          </Text>
          {!completed && !announce && <ManageLabourUpdateMenu statusUpdateId={data.id} />}
        </div>
      )}
    </div>
  );
}
