import { IconDotsVertical, IconTrash } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  DeleteLabourUpdateRequest,
  LabourUpdatesService,
  OpenAPI,
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
        color: 'var(--mantine-color-pink-6)',
      });
    },
  });

  return (
    <Menu transitionProps={{ transition: 'pop' }} withArrow position="bottom">
      <Menu.Target>
        <ActionIcon variant="subtle" color="var(--mantine-color-pink-9)">
          <IconDotsVertical size={16} stroke={1.5} />
        </ActionIcon>
      </Menu.Target>
      <Menu.Dropdown>
        <Menu.Label>Manage Update</Menu.Label>
        <Menu.Item
          color="red"
          leftSection={<IconTrash size={20} stroke={1.5} />}
          onClick={() => deleteStatusUpdate.mutate()}
        >
          Delete
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
}
