import { useState } from 'react';
import { OpenAPI, SubscriptionService, UnsubscribeFromRequest } from '@clients/labour_service';
import { Error } from '@shared/Notifications';
import { useSubscription } from '@subscription/SubscriptionContext';
import { IconDots, IconUserMinus } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import ConfirmActionModal from './ConfirmActionModal';
import baseClasses from '@shared/shared-styles.module.css';

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
        ...Error,
        title: 'Error unsubscribing',
        message: 'Something went wrong. Please try again.',
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
          <ActionIcon variant="subtle" className={baseClasses.actionMenuIcon}>
            <IconDots size={16} stroke={1.5} />
          </ActionIcon>
        </Menu.Target>
        <Menu.Dropdown className={baseClasses.actionMenuDropdown}>
          <Menu.Label className={baseClasses.actionMenuLabel}>Manage Subscription</Menu.Label>
          <Menu.Item
            className={baseClasses.actionMenuDanger}
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
