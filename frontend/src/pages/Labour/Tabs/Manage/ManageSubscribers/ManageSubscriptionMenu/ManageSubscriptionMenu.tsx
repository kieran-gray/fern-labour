import { useState } from 'react';
import {
  ApproveSubscriberRequest,
  BlockSubscriberRequest,
  RemoveSubscriberRequest,
  SubscriptionManagementService,
  UnblockSubscriberRequest,
} from '@clients/labour_service';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { Error } from '@shared/Notifications';
import {
  IconBan,
  IconCheck,
  IconCircleCheck,
  IconCircleMinus,
  IconDots,
  IconX,
} from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import baseClasses from '@shared/shared-styles.module.css';

export function ManageSubscriptionMenu({
  subscription_id,
  status,
}: {
  subscription_id: string;
  status: string;
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [action, setAction] = useState('');
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  const approveSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: ApproveSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.approveSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        ...Error,
        title: 'Error approving subscriber',
        message: 'Something went wrong. Please try again.',
      });
    },
  });

  const removeSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: RemoveSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.removeSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        ...Error,
        title: 'Error removing subscriber',
        message: 'Something went wrong. Please try again.',
      });
    },
  });

  const blockSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: BlockSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.blockSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        ...Error,
        title: 'Error blocking subscriber',
        message: 'Something went wrong. Please try again.',
      });
    },
  });

  const unblockSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: UnblockSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.unblockSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        ...Error,
        title: 'Error unblocking subscriber',
        message: 'Something went wrong. Please try again.',
      });
    },
  });

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleConfirm = () => {
    setIsModalOpen(false);
    if (action === 'remove') {
      removeSubscriberMutation.mutate();
    } else if (action === 'block') {
      blockSubscriberMutation.mutate();
    }
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
          <Menu.Label className={baseClasses.actionMenuLabel}>Manage Subscriber</Menu.Label>
          {status === 'requested' && (
            <>
              <Menu.Item
                className={baseClasses.actionMenuOk}
                leftSection={<IconCheck size={20} stroke={1.5} />}
                onClick={() => approveSubscriberMutation.mutate()}
              >
                Approve
              </Menu.Item>
              <Menu.Item
                className={baseClasses.actionMenuDanger}
                leftSection={<IconX size={20} stroke={1.5} />}
                onClick={() => removeSubscriberMutation.mutate()}
              >
                Reject
              </Menu.Item>
            </>
          )}
          {status === 'subscribed' && (
            <Menu.Item
              className={baseClasses.actionMenuDanger}
              leftSection={<IconCircleMinus size={20} stroke={1.5} />}
              onClick={() => {
                setAction('remove');
                setIsModalOpen(true);
              }}
            >
              Remove
            </Menu.Item>
          )}
          {status !== 'blocked' && (
            <Menu.Item
              className={baseClasses.actionMenuDanger}
              leftSection={<IconBan size={20} stroke={1.5} />}
              onClick={() => {
                setAction('block');
                setIsModalOpen(true);
              }}
            >
              Block
            </Menu.Item>
          )}
          {status === 'blocked' && (
            <Menu.Item
              className={baseClasses.actionMenuOk}
              leftSection={<IconCircleCheck size={20} stroke={1.5} />}
              onClick={() => unblockSubscriberMutation.mutate()}
            >
              Unblock
            </Menu.Item>
          )}
        </Menu.Dropdown>
      </Menu>
      <GenericConfirmModal
        isOpen={isModalOpen}
        title={action === 'block' ? 'Block Subscriber?' : 'Remove Subscriber?'}
        confirmText={action === 'block' ? 'Block' : 'Remove'}
        message="This can't be undone."
        onConfirm={handleConfirm}
        onCancel={handleCancel}
        isDangerous
      />
    </>
  );
}
