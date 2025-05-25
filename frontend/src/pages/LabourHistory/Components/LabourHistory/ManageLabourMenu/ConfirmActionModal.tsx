import { Button, Modal, Space, Text } from '@mantine/core';
import classes from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function ConfirmActionModal({
  onConfirm,
  onCancel,
}: {
  onConfirm: Function;
  onCancel: Function;
}) {
  const title = `Delete Labour?`;
  return (
    <Modal
      overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
      classNames={{
        content: classes.modalRoot,
        header: classes.modalHeader,
        title: classes.modalTitle,
        body: classes.modalBody,
      }}
      withCloseButton={false}
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
            onConfirm();
          }}
        >
          Delete
        </Button>
      </div>
    </Modal>
  );
}
