import { useState } from 'react';
import {
  ApiError,
  DeleteLabourUpdateRequest,
  LabourUpdatesService,
  UpdateLabourUpdateRequest,
} from '@clients/labour_service';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { Error, Success } from '@shared/Notifications';
import { IconDots, IconPencil, IconSpeakerphone, IconTrash } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ActionIcon, Menu } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
import ConfirmAnnouncementModal from './Modals/ConfirmAnnouncement';
import ConfirmDeleteModal from './Modals/ConfirmDelete';
import EditLabourUpdateModal from './Modals/EditLabourUpdate';
import baseClasses from '@shared/shared-styles.module.css';

interface ManageLabourUpdateMenuProps {
  statusUpdateId: string;
  currentMessage?: string;
}

export function ManageLabourUpdateMenu({
  statusUpdateId,
  currentMessage = '',
}: ManageLabourUpdateMenuProps) {
  const { user } = useApiAuth();
  const [editOpened, { open: openEdit, close: closeEdit }] = useDisclosure(false);
  const [announceOpened, { open: openAnnounce, close: closeAnnounce }] = useDisclosure(false);
  const [deleteOpened, { open: openDelete, close: closeDelete }] = useDisclosure(false);
  const [editMessage, setEditMessage] = useState(currentMessage);
  const queryClient = useQueryClient();

  const editStatusUpdate = useMutation({
    mutationFn: async (newMessage: string) => {
      const requestBody: UpdateLabourUpdateRequest = {
        labour_update_id: statusUpdateId,
        message: newMessage,
      };
      await LabourUpdatesService.updateLabourUpdate({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', user?.profile.sub] });
      notifications.show({
        ...Success,
        title: 'Success',
        message: `Status update edited successfully`,
      });
      closeEdit();
    },
    onError: (_) => {
      notifications.show({
        ...Error,
        title: 'Error',
        message: `Error editing status update. Please try again.`,
      });
    },
  });

  const deleteStatusUpdate = useMutation({
    mutationFn: async () => {
      const requestBody: DeleteLabourUpdateRequest = { labour_update_id: statusUpdateId };
      await LabourUpdatesService.deleteLabourUpdate({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', user?.profile.sub] });
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
      queryClient.invalidateQueries({ queryKey: ['labour', user?.profile.sub] });
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

  const handleConfirmDelete = () => {
    closeDelete();
    deleteStatusUpdate.mutate();
  };

  const handleCancelDelete = () => {
    closeDelete();
  };

  const handleConfirmAnnounce = () => {
    closeAnnounce();
    announceStatusUpdate.mutate();
  };

  const handleCancelAnnounce = () => {
    closeAnnounce();
  };

  const handleEdit = () => {
    openEdit();
    setEditMessage(currentMessage);
  };

  const handleSaveEdit = () => {
    if (editMessage.trim() === '') {
      notifications.show({
        ...Error,
        title: 'Error',
        message: 'Message cannot be empty',
      });
      return;
    }
    editStatusUpdate.mutate(editMessage.trim());
  };

  return (
    <>
      <Menu transitionProps={{ transition: 'pop' }} withArrow position="bottom">
        <Menu.Target>
          <ActionIcon variant="subtle" className={baseClasses.actionMenuIcon}>
            <IconDots size={16} stroke={1.5} />
          </ActionIcon>
        </Menu.Target>
        <Menu.Dropdown className={baseClasses.actionMenuDropdown}>
          <Menu.Label className={baseClasses.actionMenuLabel}>Manage Update</Menu.Label>
          <Menu.Item
            leftSection={<IconPencil size={20} stroke={1.5} />}
            className={baseClasses.actionMenuOk}
            onClick={() => {
              if (!statusUpdateId.startsWith('mock-')) {
                handleEdit();
              }
            }}
          >
            Edit
          </Menu.Item>
          <Menu.Item
            leftSection={<IconSpeakerphone size={20} stroke={1.5} />}
            className={baseClasses.actionMenuDanger}
            onClick={() => {
              if (!statusUpdateId.startsWith('mock-')) {
                openAnnounce();
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
                openDelete();
              }
            }}
          >
            Delete
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
      <EditLabourUpdateModal
        message={editMessage}
        opened={editOpened}
        onConfirm={handleSaveEdit}
        onCancel={closeEdit}
        onChange={setEditMessage}
      />
      <ConfirmAnnouncementModal
        message={editMessage}
        opened={announceOpened}
        onConfirm={handleConfirmAnnounce}
        onCancel={handleCancelAnnounce}
      />
      <ConfirmDeleteModal
        opened={deleteOpened}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
      />
    </>
  );
}
