import { useState } from 'react';
import {
  IconBan,
  IconCheck,
  IconCircleCheck,
  IconCircleMinus,
  IconDots,
  IconX,
} from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  ApproveSubscriberRequest,
  BlockSubscriberRequest,
  OpenAPI,
  RemoveSubscriberRequest,
  SubscriptionManagementService,
  UnblockSubscriberRequest,
} from '../../../../../../client';
import ConfirmActionModal from './ConfirmActionModal';

export function ManageSubscriptionMenu({
  subscription_id,
  status,
}: {
  subscription_id: string;
  status: string;
}) {
  const [getConfirmation, setGetConfirmation] = useState<string | undefined>(undefined);
  const [confirmed, setConfirmed] = useState<string | undefined>(undefined);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const approveSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: ApproveSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.approveSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', auth.user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        title: 'Error approving subscriber',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
  });

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

  const unblockSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: UnblockSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.unblockSubscriber({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', auth.user?.profile.sub] });
    },
    onError: () => {
      notifications.show({
        title: 'Error unblocking subscriber',
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
        {status === 'requested' && (
          <>
            <Menu.Item
              color="green"
              leftSection={<IconCheck size={20} stroke={1.5} />}
              onClick={() => approveSubscriberMutation.mutate()}
            >
              Approve
            </Menu.Item>
            <Menu.Item
              color="red"
              leftSection={<IconX size={20} stroke={1.5} />}
              onClick={() => removeSubscriberMutation.mutate()}
            >
              Reject
            </Menu.Item>
          </>
        )}
        {status === 'subscribed' && (
          <Menu.Item
            color="red"
            leftSection={<IconCircleMinus size={20} stroke={1.5} />}
            onClick={() => setGetConfirmation('remove')}
          >
            Remove
          </Menu.Item>
        )}
        {status !== 'blocked' && (
          <Menu.Item
            color="red"
            leftSection={<IconBan size={20} stroke={1.5} />}
            onClick={() => setGetConfirmation('block')}
          >
            Block
          </Menu.Item>
        )}
        {status === 'blocked' && (
          <Menu.Item
            color="green"
            leftSection={<IconCircleCheck size={20} stroke={1.5} />}
            onClick={() => unblockSubscriberMutation.mutate()}
          >
            Unblock
          </Menu.Item>
        )}
      </Menu.Dropdown>
    </Menu>
  );
}
