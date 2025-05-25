import { useState } from 'react';
import { ApiError, LabourService, OpenAPI } from '@clients/labour_service';
import { Error } from '@shared/Notifications';
import { IconDots, IconTrash } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import ConfirmActionModal from './ConfirmActionModal';
import baseClasses from '@shared/shared-styles.module.css';

export function ManageLabourMenu({ labourId }: { labourId: string }) {
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const deleteLabourMutation = useMutation({
    mutationFn: async () => {
      await LabourService.deleteLabour({ labourId });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labours', auth.user?.profile.sub] });
    },
    onError: (error) => {
      let message = 'Unknown error occurred';
      if (error instanceof ApiError) {
        try {
          const body = error.body as { description: string };
          message = body.description;
        } catch {
          // Do nothing
        }
      }
      notifications.show({
        ...Error,
        title: 'Error deleting labour',
        message,
      });
    },
  });

  const handleConfirm = () => {
    setIsModalOpen(false);
    deleteLabourMutation.mutate();
  };

  const handleCancel = () => {
    setIsModalOpen(false);
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
          <Menu.Label className={baseClasses.actionMenuLabel}>Manage Labour</Menu.Label>
          <Menu.Item
            className={baseClasses.actionMenuDanger}
            leftSection={<IconTrash size={20} stroke={1.5} />}
            onClick={() => setIsModalOpen(true)}
          >
            Delete
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
      {isModalOpen && <ConfirmActionModal onConfirm={handleConfirm} onCancel={handleCancel} />}
    </>
  );
}
