import { useState } from 'react';
import { useDeleteLabour } from '@base/shared-components/hooks';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import { IconDots, IconTrash } from '@tabler/icons-react';
import { ActionIcon, Menu } from '@mantine/core';
import baseClasses from '@shared/shared-styles.module.css';

export function ManageLabourMenu({ labourId }: { labourId: string }) {
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  const deleteLabourMutation = useDeleteLabour();

  const handleConfirm = () => {
    setIsModalOpen(false);
    deleteLabourMutation.mutate(labourId);
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
          <Menu.Label className={baseClasses.actionMenuLabel}>Manage Labour</Menu.Label>
          <Menu.Item
            className={baseClasses.actionMenuDanger}
            leftSection={<IconTrash size={20} stroke={1.5} />}
            onClick={() => setIsModalOpen(true)}
          >
            Delete
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
      <GenericConfirmModal
        isOpen={isModalOpen}
        title="Delete Labour?"
        confirmText="Delete"
        message="This can't be undone."
        onConfirm={handleConfirm}
        onCancel={handleCancel}
        isDangerous
        showCloseButton={false}
      />
    </>
  );
}
