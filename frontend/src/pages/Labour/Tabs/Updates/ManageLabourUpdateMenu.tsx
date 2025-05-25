import {
  ApiError,
  DeleteLabourUpdateRequest,
  LabourUpdatesService,
  OpenAPI,
  UpdateLabourUpdateRequest,
} from '@clients/labour_service';
import { Error, Success } from '@shared/Notifications';
import { IconDots, IconSpeakerphone, IconTrash } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import baseClasses from '@shared/shared-styles.module.css';

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
        ...Success,
        title: 'Success',
        message: `Status update deleted`,
      });
    },
    onError: (_) => {
      notifications.show({
        ...Error,
        title: 'Error',
        message: `Error deleting status update. Please try again.`,
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
        ...Success,
        title: 'Success',
        message: `Status update announced`,
      });
    },
    onError: (error) => {
      let message = 'Something went wrong. Please try again.';
      if (error instanceof ApiError) {
        message = 'Wait at least 10 seconds between announcements';
      }
      notifications.show({
        ...Error,
        title: 'Error making announcement',
        message,
      });
    },
  });

  return (
    <Menu transitionProps={{ transition: 'pop' }} withArrow position="bottom">
      <Menu.Target>
        <ActionIcon variant="subtle" className={baseClasses.actionMenuIcon}>
          <IconDots size={16} stroke={1.5} />
        </ActionIcon>
      </Menu.Target>
      <Menu.Dropdown className={baseClasses.actionMenuDropdown}>
        <Menu.Label className={baseClasses.actionMenuLabel}>Manage Update</Menu.Label>
        <Menu.Item
          leftSection={<IconSpeakerphone size={20} stroke={1.5} />}
          className={baseClasses.actionMenuDanger}
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
          className={baseClasses.actionMenuDanger}
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
