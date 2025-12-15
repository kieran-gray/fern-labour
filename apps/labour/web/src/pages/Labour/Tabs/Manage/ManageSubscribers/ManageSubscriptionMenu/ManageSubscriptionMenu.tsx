import { useState } from 'react';
import { useLabour } from '@base/contexts/LabourContext';
import {
  useApproveSubscriberV2,
  useBlockSubscriberV2,
  useRemoveSubscriberV2,
  useUnblockSubscriberV2,
} from '@base/shared-components/hooks/v2/useLabourDataV2';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import { useLabourV2Client } from '@shared/hooks';
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
  subscriptionId,
  status,
}: {
  subscriptionId: string;
  status: string;
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [action, setAction] = useState('');
  const { labourId } = useLabour();

  const client = useLabourV2Client();
  const approveSubscriberMutation = useApproveSubscriberV2(client);
  const removeSubscriberMutation = useRemoveSubscriberV2(client);
  const blockSubscriberMutation = useBlockSubscriberV2(client);
  const unblockSubscriberMutation = useUnblockSubscriberV2(client);

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleConfirm = () => {
    setIsModalOpen(false);
    if (action === 'remove') {
      removeSubscriberMutation.mutate({ labourId: labourId!, subscriptionId });
    } else if (action === 'block') {
      blockSubscriberMutation.mutate({ labourId: labourId!, subscriptionId });
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
                onClick={() =>
                  approveSubscriberMutation.mutate({ labourId: labourId!, subscriptionId })
                }
              >
                Approve
              </Menu.Item>
              <Menu.Item
                className={baseClasses.actionMenuDanger}
                leftSection={<IconX size={20} stroke={1.5} />}
                onClick={() =>
                  removeSubscriberMutation.mutate({ labourId: labourId!, subscriptionId })
                }
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
              onClick={() =>
                unblockSubscriberMutation.mutate({ labourId: labourId!, subscriptionId })
              }
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
