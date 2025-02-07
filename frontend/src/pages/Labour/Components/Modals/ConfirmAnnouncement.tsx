import { Button, Modal, Space, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './Modal.module.css';

export default function ConfirmAnnouncementModal({
  message,
  setGetConfirmation,
  setConfirmedComplete,
}: {
  message: string;
  setGetConfirmation: Function;
  setConfirmedComplete: Function;
}) {
  const [_, { close }] = useDisclosure(false);

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
      title="Make Announcement?"
    >
      <Space h="lg" />
      <Text className={classes.modalText}>
        Are you sure you want to make the following announcement to your subscribers?
      </Text>
      <div className={classes.modalInnerTextContainer}>
        <Text className={classes.modalInnerText}>{message}</Text>
      </div>
      <Space h="md" />
      <div className={baseClasses.flexRowNoBP}>
        <Button
          style={{ flex: 1, marginRight: 5 }}
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
          variant="light"
          radius="lg"
          onClick={() => {
            setConfirmedComplete(true);
            close;
          }}
        >
          Yes
        </Button>
      </div>
    </Modal>
  );
}
