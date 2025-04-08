import { useState } from 'react';
import { IconBan, IconCircleMinus, IconDots } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  BlockSubscriberRequest,
  OpenAPI,
  RemoveSubscriberRequest,
  SubscriptionManagementService,
} from '../../../../../../client';
import ConfirmActionModal from './ConfirmActionModal';

export function ManageSubscriptionMenu({ subscription_id }: { subscription_id: string }) {
  const [getConfirmation, setGetConfirmation] = useState<string | undefined>(undefined);
  const [confirmed, setConfirmed] = useState<string | undefined>(undefined);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const removeSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: RemoveSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.removeSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', auth.user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        title: 'Error removing subscriber',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
  });

  const blockSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: BlockSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.blockSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', auth.user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        title: 'Error blocking subscriber',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
  });

  if (getConfirmation) {
    if (confirmed) {
      if (getConfirmation === 'remove') {
        removeSubscriberMutation.mutate();
      } else if (getConfirmation === 'block') {
        blockSubscriberMutation.mutate();
      }
      setGetConfirmation(undefined);
      setConfirmed(undefined);
    } else {
      return (
        <ConfirmActionModal
          setGetConfirmation={setGetConfirmation}
          setConfirmed={setConfirmed}
          action={getConfirmation}
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
          onClick={() => setGetConfirmation('remove')}
        >
          Remove
        </Menu.Item>
        <Menu.Item
          color="red"
          leftSection={<IconBan size={20} stroke={1.5} />}
          onClick={() => setGetConfirmation('block')}
        >
          Block
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
}
