import { Button, Modal, Space, Textarea } from '@mantine/core';
import classes from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function EditLabourUpdateModal({
  message,
  opened,
  onConfirm,
  onChange,
  onCancel,
}: {
  message: string;
  opened: boolean;
  onConfirm: Function;
  onChange: Function;
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
      opened={opened}
      centered
      closeOnClickOutside
      onClose={() => onCancel()}
      title="Edit Status Update"
    >
      <Space h="lg" />
      <Textarea
        label="Your status update"
        placeholder="Enter your updated message..."
        value={message}
        onChange={(event) => onChange(event.currentTarget.value)}
        minRows={3}
        maxRows={6}
        radius="lg"
        styles={{ label: { paddingLeft: 10 } }}
        classNames={{ input: baseClasses.input, label: baseClasses.description }}
        mb={20}
        autosize
      />
      <div className={baseClasses.flexRowNoBP}>
        <Button
          style={{ flex: 1, marginRight: 5 }}
          radius="lg"
          variant="light"
          onClick={() => onCancel()}
        >
          Cancel
        </Button>
        <Button
          style={{ flex: 1, marginLeft: 5 }}
          radius="lg"
          onClick={() => onConfirm()}
          disabled={message.trim() === ''}
        >
          Save Changes
        </Button>
      </div>
    </Modal>
  );
}
