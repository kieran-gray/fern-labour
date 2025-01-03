
import { Text, Modal, Space, Button, Group } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from './ConfirmCompleteLabourModal.module.css';
import baseClasses from '../shared-styles.module.css'


export default function ConfirmCompleteLabourModal({ setConfirmedComplete }: { setConfirmedComplete: Function }) {
  const [opened, { open, close }] = useDisclosure(false); 

    return (
    <Modal overlayProps={{ backgroundOpacity: 0.55, blur: 3 }} classNames={{content: classes.root, header:classes.modalHeader, title: classes.modalTitle, body:classes.modalBody, close: classes.closeButton}} opened={true} onClose={close} title="End your labour?">
        <Space h="lg"></Space>
        <Text className={classes.modalText}>Are you sure you want to end your current labour?</Text>
        <Space h="md"></Space>
        <div className={baseClasses.flexRowNoBP}>
            <Button style={{flex: 1, "margin-right": 5}} radius="lg" onClick={() => {setConfirmedComplete(false); close()}}>Cancel</Button>
            <Button style={{flex: 1, "margin-left": 5}} variant="light" radius="lg" onClick={() => {setConfirmedComplete(true); close}}>Yes</Button>
        </div>
    </Modal>
    )
}