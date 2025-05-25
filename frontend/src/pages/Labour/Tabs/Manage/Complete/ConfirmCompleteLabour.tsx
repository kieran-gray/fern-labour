import { Button, Modal, Space, Text } from '@mantine/core';
import classes from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function ConfirmCompleteLabourModal({
  onConfirm,
  onCancel,
}: {
  onConfirm: Function;
  onCancel: Function;
}) {
  return (
    <Modal
      overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
      classNames={{
        content: classes.modalRoot,
        header: classes.modalHeader,
        title: classes.modalTitle,
        body: classes.modalBody,
        close: classes.modalCloseButton,
      }}
      opened
      centered
      onClose={() => {
        onCancel();
      }}
      title="Complete your labour?"
    >
      <Space h="lg" />
      <Text className={classes.modalText}>
        Are you sure you want to complete your current labour?
      </Text>
      <Space h="md" />
      <div className={baseClasses.flexRowNoBP}>
        <Button
          style={{ flex: 1, marginRight: 5 }}
          radius="lg"
          onClick={() => {
            onCancel();
          }}
        >
          Cancel
        </Button>
        <Button
          style={{ flex: 1, marginLeft: 5 }}
          variant="light"
          radius="lg"
          onClick={() => {
            onConfirm();
          }}
        >
          Yes
        </Button>
      </div>
    </Modal>
  );
}
