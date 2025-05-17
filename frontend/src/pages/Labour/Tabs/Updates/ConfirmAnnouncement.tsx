import { Button, Modal, Space, Text } from '@mantine/core';
import classes from '../../../../shared-components/Modal.module.css';
import baseClasses from '../../../../shared-components/shared-styles.module.css';

export default function ConfirmAnnouncementModal({
  message,
  onConfirm,
  onCancel,
}: {
  message: string;
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
        close: classes.closeButton,
      }}
      opened
      centered
      closeOnClickOutside
      onClose={() => {
        onCancel();
      }}
      title="Make Announcement?"
    >
      <Space h="lg" />
      <Text className={classes.modalText}>You can't delete an announcement.</Text>
      <div className={classes.modalInnerTextContainer}>
        <Text className={classes.modalInnerText}>{message}</Text>
      </div>
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
