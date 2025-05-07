import { useSearchParams } from 'react-router-dom';
import { Button, Modal, Text } from '@mantine/core';
import modalClasses from '../../../../shared-components/Modal.module.css';
import classes from './SubscriptionRequestedModal.module.css';

type CloseFunctionType = (...args: any[]) => void;

export default function SubscriptionRequestedModal({
  opened,
  close,
}: {
  opened: boolean;
  close: CloseFunctionType;
}) {
  const [searchParams, setSearchParams] = useSearchParams();

  return (
    <Modal
      opened={opened}
      closeOnClickOutside
      onClose={() => {
        searchParams.delete('prompt');
        setSearchParams(searchParams);
        close();
      }}
      title="Request Sent"
      centered
      overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
      classNames={{
        content: modalClasses.modalRoot,
        header: modalClasses.modalHeader,
        title: modalClasses.modalTitle,
        body: modalClasses.modalBody,
        close: modalClasses.closeButton,
      }}
    >
      <div style={{ padding: '20px 10px 10px' }}>
        <div className={classes.flexColumn}>
          <Text ta="center">
            Your request to join a labour circle has been sent.
            <br />
            <br />
            They'll need to approve your request before you can view updates or messages.
            <br />
            <br />
            You'll get an email as soon as you're approved, thanks for your patience! 💛
            <br />
            <br />
          </Text>
        </div>
        <div className={classes.flexRowNoBP}>
          <Button
            style={{ flex: 1, marginRight: 5, width: '100%' }}
            radius="lg"
            variant="light"
            onClick={() => {
              searchParams.delete('prompt');
              setSearchParams(searchParams);
              close();
            }}
          >
            Close
          </Button>
        </div>
      </div>
    </Modal>
  );
}
