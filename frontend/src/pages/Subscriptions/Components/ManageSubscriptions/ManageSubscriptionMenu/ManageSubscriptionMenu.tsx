import { useState } from 'react';
import { IconDots, IconUserMinus } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { OpenAPI, SubscriptionService, UnsubscribeFromRequest } from '../../../../../client';
import ConfirmActionModal from './ConfirmActionModal';

export function ManageSubscriptionMenu({ labour_id }: { labour_id: string }) {
  const [getConfirmation, setGetConfirmation] = useState<boolean | undefined>(undefined);
  const [confirmed, setConfirmed] = useState<string | undefined>(undefined);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const unsubscribeMutation = useMutation({
    mutationFn: async () => {
      const requestBody: UnsubscribeFromRequest = { labour_id };
      await SubscriptionService.unsubscribeFrom({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['subscriber_subscriptions', auth.user?.profile.sub],
      });
    },
    onError: () => {
      notifications.show({
        title: 'Error unsubscribing',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
  });

  if (getConfirmation) {
    if (confirmed) {
      unsubscribeMutation.mutate();
      setGetConfirmation(false);
      setConfirmed(undefined);
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
          <IconDots size={16} stroke={1.5} />
        </ActionIcon>
      </Menu.Target>
      <Menu.Dropdown>
        <Menu.Label>Manage Subscription</Menu.Label>
        <Menu.Item
          color="red"
          leftSection={<IconUserMinus size={20} stroke={1.5} />}
          onClick={() => setGetConfirmation(true)}
        >
          Unsubscribe
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
}
