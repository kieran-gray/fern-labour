import { Badge, Group, LoadingOverlay, Text } from '@mantine/core';
import { ManageLabourUpdateMenu } from './ManageLabourUpdateMenu';
import classes from './LabourUpdates.module.css';

export interface LabourUpdateProps {
  id: string;
  sentTime: string;
  class: string;
  icon: string;
  badgeColor: string;
  badgeText: string;
  text: string;
  visibility: string;
  showMenu: boolean;
  showFooter: boolean;
}

export function LabourUpdate({ data }: { data: LabourUpdateProps }) {
  return (
    <div className={data.class}>
      <LoadingOverlay visible={data.id === 'placeholder'} />
      <Group>
        <Text>{data.icon}</Text>
        <Badge visibleFrom="xs" variant="filled" size="md" radius="md" bg={data.badgeColor}>
          {data.badgeText}
        </Badge>
        <Badge hiddenFrom="xs" variant="filled" size="sm" radius="md" bg={data.badgeColor}>
          {data.badgeText}
        </Badge>

        <div style={{ flexGrow: 1 }} />
        <Text size="xs" c="var(--mantine-color-gray-9)">
          {data.sentTime}
        </Text>
      </Group>
      <Text pt="sm" size="md" fw="400" visibleFrom="xs">
        {data.text}
      </Text>
      <Text pt="sm" size="sm" fw="400" hiddenFrom="xs">
        {data.text}
      </Text>
      {}
      {data.showFooter && (
        <div className={classes.messageFooter}>
          <Text size="xs">{data?.visibility}</Text>
          {data.showMenu && <ManageLabourUpdateMenu statusUpdateId={data.id} />}
        </div>
      )}
    </div>
  );
}
