import { IconDots, IconSpeakerphone, IconTrash } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  ApiError,
  DeleteLabourUpdateRequest,
  LabourUpdatesService,
  OpenAPI,
  UpdateLabourUpdateRequest,
} from '../../../../clients/labour_service';

export function ManageLabourUpdateMenu({ statusUpdateId }: { statusUpdateId: string }) {
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const deleteStatusUpdate = useMutation({
    mutationFn: async () => {
      const requestBody: DeleteLabourUpdateRequest = { labour_update_id: statusUpdateId };
      await LabourUpdatesService.deleteLabourUpdate({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      notifications.show({
        title: 'Success',
        message: `Status update deleted`,
        radius: 'lg',
        color: 'var(--mantine-color-green-3)',
      });
    },
    onError: (_) => {
      notifications.show({
        title: 'Error',
        message: `Error deleting status update. Please try again.`,
        radius: 'lg',
        color: 'var(--mantine-color-primary-6)',
      });
    },
  });

  const announceStatusUpdate = useMutation({
    mutationFn: async () => {
      const requestBody: UpdateLabourUpdateRequest = {
        labour_update_id: statusUpdateId,
        labour_update_type: 'announcement',
      };
      await LabourUpdatesService.updateLabourUpdate({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      notifications.show({
        title: 'Success',
        message: `Status update announced`,
        radius: 'lg',
        color: 'var(--mantine-color-green-3)',
      });
    },
    onError: (error) => {
      let message = 'Something went wrong. Please try again.';
      if (error instanceof ApiError) {
        message = 'Wait at least 10 seconds between announcements';
      }
      notifications.show({
        title: 'Error making announcement',
        message,
        radius: 'lg',
        color: 'var(--mantine-color-primary-7)',
      });
    },
  });

  return (
    <Menu transitionProps={{ transition: 'pop' }} withArrow position="bottom">
      <Menu.Target>
        <ActionIcon variant="subtle" color="var(--mantine-color-gray-8)">
          <IconDots size={16} stroke={1.5} />
        </ActionIcon>
      </Menu.Target>
      <Menu.Dropdown>
        <Menu.Label>Manage Update</Menu.Label>
        <Menu.Item
          leftSection={<IconSpeakerphone size={20} stroke={1.5} />}
          style={{color: 'light-dark(red, var(--mantine-color-gray-1))'}}
          onClick={() => {
            if (!statusUpdateId.startsWith('mock-')) {
              announceStatusUpdate.mutate();
            }
          }}
        >
          Announce
        </Menu.Item>
        <Menu.Divider />
        <Menu.Item
          leftSection={<IconTrash size={20} stroke={1.5} />}
          style={{color: 'light-dark(red, var(--mantine-color-gray-1))'}}
          onClick={() => {
            if (!statusUpdateId.startsWith('mock-')) {
              deleteStatusUpdate.mutate();
            }
          }}
        >
          Delete
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
}
