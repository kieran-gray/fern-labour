import { useState } from 'react';
import { SubscriberRole } from '@base/clients/labour_service';
import { useLabourSession } from '@base/contexts/LabourSessionContext';
import { useLabourV2Client } from '@base/hooks';
import {
  useApproveSubscriberV2,
  useBlockSubscriberV2,
  useRemoveSubscriberV2,
  useUnblockSubscriberV2,
} from '@base/hooks/useLabourData';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import {
  IconBan,
  IconCheck,
  IconCircleCheck,
  IconCircleMinus,
  IconDots,
  IconSwitchHorizontal,
  IconX,
} from '@tabler/icons-react';
import { ActionIcon, Menu } from '@mantine/core';
import { ChangeRoleModal } from './ChangeRoleModal';
import baseClasses from '@shared/shared-styles.module.css';

export function ManageSubscriptionMenu({
  subscriptionId,
  status,
  currentRole,
}: {
  subscriptionId: string;
  status: string;
  currentRole?: SubscriberRole;
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isRoleModalOpen, setIsRoleModalOpen] = useState(false);
  const [action, setAction] = useState('');
  const { labourId } = useLabourSession();

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

  const handleRoleChange = async (newRole: SubscriberRole) => {
    setIsRoleModalOpen(false);
    await client.updateSubscriberRole(labourId!, subscriptionId, newRole);
    // Refresh the data to show updated role
    window.location.reload();
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
            <>
              <Menu.Item
                className={baseClasses.actionMenuDefault}
                leftSection={<IconSwitchHorizontal size={20} stroke={1.5} />}
                onClick={() => setIsRoleModalOpen(true)}
              >
                Change Role
              </Menu.Item>
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
            </>
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
      {currentRole && (
        <ChangeRoleModal
          isOpen={isRoleModalOpen}
          currentRole={currentRole}
          onConfirm={handleRoleChange}
          onCancel={() => setIsRoleModalOpen(false)}
        />
      )}
    </>
  );
}
