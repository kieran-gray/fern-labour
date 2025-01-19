import { Text, Modal, Space, Button } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from './Modal.module.css';
import baseClasses from '../../../../shared-components/shared-styles.module.css'


export default function ConfirmRemoveSubscriberModal({ setGetConfirmation, setConfirmed }: { setGetConfirmation: Function, setConfirmed: Function }) {
  const [_, { close }] = useDisclosure(false);

    return (
    <Modal overlayProps={{ backgroundOpacity: 0.55, blur: 3 }} classNames={{content: classes.root, header:classes.modalHeader, title: classes.modalTitle, body:classes.modalBody, close: classes.closeButton}} opened={true} onClose={close} title="Remove Subscriber?">
        <Space h="lg"></Space>
        <Text className={classes.modalText}>This can't be undone.</Text>
        <Space h="md"></Space>
        <div className={baseClasses.flexRowNoBP}>
            <Button style={{flex: 1, marginRight: 5}} variant="light" radius="lg" onClick={() => {setGetConfirmation(false); close}}>Cancel</Button>
            <Button style={{flex: 1, marginLeft: 5}} radius="lg" onClick={() => {setConfirmed(true); close}}>Remove</Button>
        </div>
    </Modal>
    )
}