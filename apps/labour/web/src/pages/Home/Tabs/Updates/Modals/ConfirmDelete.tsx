import { Button, Group, Modal, Stack, Text } from '@mantine/core';
import classes from '@components/Modal.module.css';

export default function ConfirmDeleteModal({
  onConfirm,
  onCancel,
  opened,
}: {
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
      onClose={() => onCancel()}
      title="Delete status update?"
    >
      <Stack gap="md">
        <Text className={classes.modalText}>This can't be undone.</Text>
        <Group justify="flex-end" gap="sm">
          <Button size="sm" radius="md" variant="default" onClick={() => onCancel()}>
            Cancel
          </Button>
          <Button size="sm" radius="md" color="red" onClick={() => onConfirm()}>
            Delete
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
}
