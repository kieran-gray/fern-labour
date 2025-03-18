import { useState } from 'react';
import { IconArrowRight, IconDotsVertical, IconTrash } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { ApiError, LabourService, OpenAPI } from '../../../../../client';
import ConfirmActionModal from './ConfirmActionModal';

export function ManageLabourMenu({ labourId }: { labourId: string }) {
  const [getConfirmation, setGetConfirmation] = useState<boolean>(false);
  const [confirmed, setConfirmed] = useState<boolean>(false);
  const auth = useAuth();
  const navigate = useNavigate();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const blockSubscriberMutation = useMutation({
    mutationFn: async () => {
      await LabourService.deleteLabourApiV1LabourDeleteLabourIdDelete({ labourId });
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

  if (getConfirmation) {
    if (confirmed) {
      blockSubscriberMutation.mutate();
      setGetConfirmation(false);
      setConfirmed(false);
    } else {
      return (
        <ConfirmActionModal setGetConfirmation={setGetConfirmation} setConfirmed={setConfirmed} />
      );
    }
  }

  return (
    <Menu transitionProps={{ transition: 'pop' }} withArrow position="bottom">
      <Menu.Target>
        <ActionIcon variant="subtle" color="var(--mantine-color-pink-9)">
          <IconDotsVertical size={16} stroke={1.5} />
        </ActionIcon>
      </Menu.Target>
      <Menu.Dropdown>
        <Menu.Label>Manage Labour</Menu.Label>
        <Menu.Item
          rightSection={<IconArrowRight size={20} stroke={1.5} />}
          color="var(--mantine-color-gray-8)"
          onClick={() => {
            queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
            navigate(`/?labourId=${labourId}`);
          }}
        >
          View Labour
        </Menu.Item>
        <Menu.Divider />
        <Menu.Item
          color="red"
          leftSection={<IconTrash size={20} stroke={1.5} />}
          onClick={() => setGetConfirmation(true)}
        >
          Delete
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
}
