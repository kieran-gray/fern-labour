import { useState } from 'react';
import { useSubscription } from '@base/contexts/SubscriptionContext';
import { useUnsubscribeFrom } from '@base/shared-components/hooks/useSubscriptionData';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import { IconDots, IconUserMinus } from '@tabler/icons-react';
import { ActionIcon, Menu } from '@mantine/core';
import baseClasses from '@shared/shared-styles.module.css';

export function ManageSubscriptionMenu({ labour_id }: { labour_id: string }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { setSubscriptionId } = useSubscription();

  const unsubscribeMutation = useUnsubscribeFrom();

  const handleConfirm = async () => {
    setIsModalOpen(false);
    await unsubscribeMutation.mutateAsync(labour_id);
    setSubscriptionId('');
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
