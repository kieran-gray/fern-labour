import { useState } from 'react';
import { IconDotsVertical, IconTrash } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { ApiError, LabourService, OpenAPI } from '../../../../../clients/labour_service';
import ConfirmActionModal from './ConfirmActionModal';

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
        title: 'Error deleting labour',
        message,
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
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
          <ActionIcon variant="subtle" color="var(--mantine-color-pink-9)">
            <IconDotsVertical size={16} stroke={1.5} />
          </ActionIcon>
        </Menu.Target>
        <Menu.Dropdown>
          <Menu.Label>Manage Labour</Menu.Label>
          <Menu.Item
            color="red"
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
