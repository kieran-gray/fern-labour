import { useState } from 'react';
import { IconBan, IconCircleMinus, IconDots } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { BirthingPersonService, OpenAPI, RemoveSubscriberRequest } from '../../../../client';
import ConfirmActionModal from './ConfirmActionModal';

export function ManageSubscriberMenu({ subscriber_id }: { subscriber_id: string }) {
  const [getConfimation, setGetConfimation] = useState<string | undefined>(undefined);
  const [confirmed, setConfirmed] = useState<string | undefined>(undefined);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();
  const banEnabled = false;

  const removeSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: RemoveSubscriberRequest = { subscriber_id };
      await BirthingPersonService.removeSubscriberApiV1BirthingPersonRemoveSubscriberPost({
        requestBody,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscribers', auth.user?.profile.sub] });
    },
    onError: (error) => {
      console.error('Error removing subscriber', error);
    },
  });

  const blockSubscriberMutation = useMutation({
    mutationFn: async () => {
      // TODO: Implement block subscriber mutation
      console.log(subscriber_id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscribers', auth.user?.profile.sub] });
    },
    onError: (error) => {
      console.error('Error removing subscriber', error);
    },
  });

  if (getConfimation) {
    if (confirmed) {
      if (getConfimation === 'remove') {
        removeSubscriberMutation.mutate();
      } else if (getConfimation === 'block') {
        blockSubscriberMutation.mutate();
      }
      setGetConfimation(undefined);
      setConfirmed(undefined);
    } else {
      return (
        <ConfirmActionModal
          setGetConfirmation={setGetConfimation}
          setConfirmed={setConfirmed}
          action={getConfimation}
        />
      );
    }
  }

  return (
    <Menu transitionProps={{ transition: 'pop' }} withArrow position="bottom">
      <Menu.Target>
        <ActionIcon variant="subtle" color="var(--mantine-color-pink-9)">
          <IconDots size={16} stroke={1.5} />
        </ActionIcon>
      </Menu.Target>
      <Menu.Dropdown>
        <Menu.Label>Manage Subscriber</Menu.Label>
        <Menu.Item
          color="red"
          leftSection={<IconCircleMinus size={20} stroke={1.5} />}
          onClick={() => setGetConfimation('remove')}
        >
          Remove
        </Menu.Item>
        {banEnabled && (
          <Menu.Item
            color="red"
            leftSection={<IconBan size={20} stroke={1.5} />}
            onClick={() => setGetConfimation('block')}
          >
            Block
          </Menu.Item>
        )}
      </Menu.Dropdown>
    </Menu>
  );
}
