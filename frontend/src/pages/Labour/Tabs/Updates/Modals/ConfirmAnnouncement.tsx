import { Button, Modal, Space, Text } from '@mantine/core';
import classes from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function ConfirmAnnouncementModal({
  message,
  onConfirm,
  onCancel,
  opened,
}: {
  message: string;
  onConfirm: Function;
  onCancel: Function;
  opened: boolean;
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
      opened={opened}
      centered
      closeOnClickOutside
      onClose={() => {
        onCancel();
      }}
      title="Make Announcement?"
    >
      <Space h="lg" />
      <Text className={classes.modalText}>Announcements can't be edited or deleted.</Text>
      <div className={classes.modalInnerTextContainer}>
        <Text className={classes.modalInnerText}>{message}</Text>
      </div>
      <Space h="md" />
      <div className={baseClasses.flexRowNoBP}>
        <Button
          style={{ flex: 1, marginRight: 5 }}
          radius="lg"
          variant="light"
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
          Yes
        </Button>
      </div>
    </Modal>
  );
}
