import { Button, Modal, Space, Text } from '@mantine/core';
import classes from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

interface GenericConfirmModalProps {
  /** Whether the modal is open */
  isOpen: boolean;
  /** The title displayed in the modal header */
  title: string;
  /** The text displayed in the confirm button */
  confirmText: string;
  /** The message displayed in the modal body */
  message?: string;
  /** Function called when user confirms the action */
  onConfirm: () => void;
  /** Function called when user cancels or closes the modal */
  onCancel: () => void;
  /** Whether this is a dangerous action (affects button styling) */
  isDangerous?: boolean;
  /** Whether to show the close button in header */
  showCloseButton?: boolean;
  /** Whether clicking outside closes the modal */
  closeOnClickOutside?: boolean;
}

export function GenericConfirmModal({
  isOpen,
  title,
  confirmText,
  message = "This can't be undone.",
  onConfirm,
  onCancel,
  isDangerous = false,
  showCloseButton = true,
  closeOnClickOutside = true,
}: GenericConfirmModalProps) {
  return (
    <Modal
      overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
      classNames={{
        content: classes.modalRoot,
        header: classes.modalHeader,
        title: classes.modalTitle,
        body: classes.modalBody,
        close: classes.closeButton,
      }}
      opened={isOpen}
      centered
      closeOnClickOutside={closeOnClickOutside}
      withCloseButton={showCloseButton}
      onClose={onCancel}
      title={title}
    >
      <Space h="lg" />
      <Text className={classes.modalText}>{message}</Text>
      <Space h="md" />
      <div className={baseClasses.flexRowNoBP}>
        <Button style={{ flex: 1, marginRight: 5 }} variant="light" radius="lg" onClick={onCancel}>
          Cancel
        </Button>
        <Button
          style={{ flex: 1, marginLeft: 5 }}
          radius="lg"
          color={isDangerous ? 'red' : undefined}
          onClick={onConfirm}
        >
          {confirmText}
        </Button>
      </div>
    </Modal>
  );
}
