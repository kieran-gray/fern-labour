import { Text, Modal, Space, Button } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from './Modal.module.css';
import baseClasses from '../../../../shared-components/shared-styles.module.css'


export default function ConfirmCompleteLabourModal({ setGetConfirmation, setConfirmedComplete }: { setGetConfirmation: Function, setConfirmedComplete: Function }) {
  const [_, { close }] = useDisclosure(false);

    return (
    <Modal overlayProps={{ backgroundOpacity: 0.55, blur: 3 }} classNames={{content: classes.root, header:classes.modalHeader, title: classes.modalTitle, body:classes.modalBody, close: classes.closeButton}} opened={true} onClose={close} title="Complete your labour?">
        <Space h="lg"></Space>
        <Text className={classes.modalText}>Are you sure you want to complete your current labour?</Text>
        <Space h="md"></Space>
        <div className={baseClasses.flexRowNoBP}>
            <Button style={{flex: 1, marginRight: 5}} radius="lg" onClick={() => {setGetConfirmation(false); close}}>Cancel</Button>
            <Button style={{flex: 1, marginLeft: 5}} variant="light" radius="lg" onClick={() => {setConfirmedComplete(true); close}}>Yes</Button>
        </div>
    </Modal>
    )
}