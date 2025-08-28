import { useState } from 'react';
import { SubscriptionService, UnsubscribeFromRequest } from '@clients/labour_service';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { Error } from '@shared/Notifications';
import { useSubscription } from '@subscription/SubscriptionContext';
import { IconDots, IconUserMinus } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import baseClasses from '@shared/shared-styles.module.css';

export function ManageSubscriptionMenu({ labour_id }: { labour_id: string }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { setSubscriptionId } = useSubscription();
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  const unsubscribeMutation = useMutation({
    mutationFn: async () => {
      const requestBody: UnsubscribeFromRequest = { labour_id };
      await SubscriptionService.unsubscribeFrom({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['subscriber_subscriptions', user?.profile.sub],
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
      <GenericConfirmModal
        isOpen={isModalOpen}
        title="Unsubscribe?"
        confirmText="Unsubscribe"
        message="This can't be undone."
        onConfirm={handleConfirm}
        onCancel={handleCancel}
        isDangerous
      />
    </>
  );
}
