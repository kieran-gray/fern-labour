import { Button, Modal, Space, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './ConfirmActionModal.module.css';

export default function ConfirmActionModal({
  setGetConfirmation,
  setConfirmed,
}: {
  setGetConfirmation: Function;
  setConfirmed: Function;
}) {
  const [_, { close }] = useDisclosure(false);
  const title = `Delete Labour?`;
  return (
    <Modal
      overlayProps={{ backgroundOpacity: 0.55, blur: 3 }}
      classNames={{
        content: classes.root,
        header: classes.modalHeader,
        title: classes.modalTitle,
        body: classes.modalBody,
        close: classes.closeButton,
      }}
      opened
      onClose={close}
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
            setGetConfirmation(false);
            close;
          }}
        >
          Cancel
        </Button>
        <Button
          style={{ flex: 1, marginLeft: 5 }}
          radius="lg"
          onClick={() => {
            setConfirmed(true);
            close;
          }}
        >
          Delete
        </Button>
      </div>
    </Modal>
  );
}
