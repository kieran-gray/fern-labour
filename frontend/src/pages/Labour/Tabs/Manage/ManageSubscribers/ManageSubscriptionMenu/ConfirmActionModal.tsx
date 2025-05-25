import { Button, Modal, Space, Text } from '@mantine/core';
import classes from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function ConfirmActionModal({
  onConfirm,
  onCancel,
  action,
}: {
  onConfirm: Function;
  onCancel: Function;
  action: string;
}) {
  const displayAction = action === 'block' ? 'Block' : 'Remove';
  const title = `${displayAction} Subscriber?`;
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
      opened
      centered
      closeOnClickOutside
      onClose={() => {
        onCancel();
      }}
      title={title}
    >
      <Space h="lg" />
      <Text className={classes.modalText}>This can't be undone.</Text>
      <Space h="md" />
      <div className={baseClasses.flexRowNoBP}>
        <Button
          style={{ flex: 1, marginRight: 5 }}
          variant="light"
          radius="lg"
          onClick={() => {
            onCancel();
          }}
        >
          Cancel
        </Button>
        <Button
          style={{ flex: 1, marginLeft: 5 }}
          radius="lg"
          onClick={() => {
            onConfirm(action);
          }}
        >
          {displayAction}
        </Button>
      </div>
    </Modal>
  );
}
