import { useState } from 'react';
import {
  useApproveSubscriber,
  useBlockSubscriber,
  useRemoveSubscriber,
  useUnblockSubscriber,
} from '@base/shared-components/hooks';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import {
  IconBan,
  IconCheck,
  IconCircleCheck,
  IconCircleMinus,
  IconDots,
  IconX,
} from '@tabler/icons-react';
import { ActionIcon, Menu } from '@mantine/core';
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

  const approveSubscriberMutation = useApproveSubscriber();
  const removeSubscriberMutation = useRemoveSubscriber();
  const blockSubscriberMutation = useBlockSubscriber();
  const unblockSubscriberMutation = useUnblockSubscriber();

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleConfirm = () => {
    setIsModalOpen(false);
    if (action === 'remove') {
      removeSubscriberMutation.mutate(subscription_id);
    } else if (action === 'block') {
      blockSubscriberMutation.mutate(subscription_id);
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
                onClick={() => approveSubscriberMutation.mutate(subscription_id)}
              >
                Approve
              </Menu.Item>
              <Menu.Item
                className={baseClasses.actionMenuDanger}
                leftSection={<IconX size={20} stroke={1.5} />}
                onClick={() => removeSubscriberMutation.mutate(subscription_id)}
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
              onClick={() => unblockSubscriberMutation.mutate(subscription_id)}
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
