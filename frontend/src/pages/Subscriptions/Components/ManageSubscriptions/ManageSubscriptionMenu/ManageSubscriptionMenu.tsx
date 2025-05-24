import { useState } from 'react';
import { IconDots, IconUserMinus } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  OpenAPI,
  SubscriptionService,
  UnsubscribeFromRequest,
} from '../../../../../clients/labour_service';
import { useSubscription } from '../../../../Subscription/SubscriptionContext';
import ConfirmActionModal from './ConfirmActionModal';

export function ManageSubscriptionMenu({ labour_id }: { labour_id: string }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { setSubscriptionId } = useSubscription();
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
      setSubscriptionId('');
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

  const handleConfirm = () => {
    setIsModalOpen(false);
    unsubscribeMutation.mutate();
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <>
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
            onClick={() => setIsModalOpen(true)}
          >
            Unsubscribe
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
      {isModalOpen && <ConfirmActionModal onConfirm={handleConfirm} onCancel={handleCancel} />}
    </>
  );
}
