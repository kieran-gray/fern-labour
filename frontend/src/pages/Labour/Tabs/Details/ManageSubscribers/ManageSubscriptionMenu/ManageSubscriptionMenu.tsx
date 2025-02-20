import { useState } from 'react';
import { IconBan, IconCircleMinus, IconDots } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Menu } from '@mantine/core';
import {
  BlockSubscriberRequest,
  OpenAPI,
  RemoveSubscriberRequest,
  SubscriptionManagementService,
} from '../../../../../../client';
import ConfirmActionModal from './ConfirmActionModal';

export function ManageSubscriptionMenu({ subscription_id }: { subscription_id: string }) {
  const [getConfimation, setGetConfimation] = useState<string | undefined>(undefined);
  const [confirmed, setConfirmed] = useState<string | undefined>(undefined);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const removeSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: RemoveSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.removeSubscriberApiV1SubscriptionManagementRemoveSubscriberPut(
        {
          requestBody,
        }
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', auth.user?.profile.sub] });
    },
    onError: (error) => {
      console.error('Error removing subscriber', error);
    },
  });

  const blockSubscriberMutation = useMutation({
    mutationFn: async () => {
      const requestBody: BlockSubscriberRequest = { subscription_id };
      await SubscriptionManagementService.blockSubscriberApiV1SubscriptionManagementBlockSubscriberPut(
        {
          requestBody,
        }
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labour_subscriptions', auth.user?.profile.sub] });
    },
    onError: (error) => {
      console.error('Error blocking subscriber', error);
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
        <Menu.Item
          color="red"
          leftSection={<IconBan size={20} stroke={1.5} />}
          onClick={() => setGetConfimation('block')}
        >
          Block
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
}
