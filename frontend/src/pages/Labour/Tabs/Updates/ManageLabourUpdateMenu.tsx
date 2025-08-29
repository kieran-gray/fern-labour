import { useState } from 'react';
import { UpdateLabourUpdateRequest } from '@clients/labour_service';
import { useDeleteLabourUpdate, useEditLabourUpdate } from '@shared/hooks';
import { Error } from '@shared/Notifications';
import { IconDots, IconPencil, IconSpeakerphone, IconTrash } from '@tabler/icons-react';
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
  const [editOpened, { open: openEdit, close: closeEdit }] = useDisclosure(false);
  const [announceOpened, { open: openAnnounce, close: closeAnnounce }] = useDisclosure(false);
  const [deleteOpened, { open: openDelete, close: closeDelete }] = useDisclosure(false);
  const [editMessage, setEditMessage] = useState(currentMessage);

  const editStatusUpdateMutation = useEditLabourUpdate();
  const deleteStatusUpdateMutation = useDeleteLabourUpdate();

  const handleEditStatusUdpate = async (newMessage: string) => {
    const requestBody: UpdateLabourUpdateRequest = {
      labour_update_id: statusUpdateId,
      message: newMessage,
    };
    await editStatusUpdateMutation.mutateAsync(requestBody);
    closeEdit();
  };
  const handleAnnounceStatusUdpate = async () => {
    const requestBody: UpdateLabourUpdateRequest = {
      labour_update_id: statusUpdateId,
      labour_update_type: 'announcement',
    };
    await editStatusUpdateMutation.mutateAsync(requestBody);
  };

  const handleConfirmDelete = () => {
    closeDelete();
    deleteStatusUpdateMutation.mutate(statusUpdateId);
  };

  const handleCancelDelete = () => {
    closeDelete();
  };

  const handleConfirmAnnounce = () => {
    closeAnnounce();
    handleAnnounceStatusUdpate();
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
    handleEditStatusUdpate(editMessage.trim());
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
