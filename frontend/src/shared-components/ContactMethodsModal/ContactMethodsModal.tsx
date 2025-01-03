
import { useState } from "react";
import { SubscriberDTO, SubscriberResponse, RegisterSubscriberRequest } from "../../client";
import { useAuth } from "react-oidc-context";
import { Text, Modal, Space, Button, Group, Checkbox } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from './ContactMethodsModal.module.css';


export default function ContactMethodsModal({ name, promptForContactMethods }: { name: string, promptForContactMethods: Function }) {
  const [email, setEmail] = useState(true);
  const [sms, setSMS] = useState(true);
  const [opened, { open, close }] = useDisclosure(false);
  const auth = useAuth();

  const registerSubscriber = async (body: RegisterSubscriberRequest): Promise<SubscriberDTO | null> => {
    const headers = {
      'Authorization': `Bearer ${auth.user?.access_token}`,
      'Content-Type': 'application/json'
    }
    console.log(body)
    const response = await fetch(
      'http://localhost:8000/api/v1/subscriber/register',
      { method: 'POST', headers: headers, body: JSON.stringify(body) }
    );
    if (response.ok) {
      const data: SubscriberResponse = await response.json()
      return data.subscriber
    } else {
      return null
    }
  }

  const contactMethodsDialogSubmitted = async ({sms, email}: {sms: boolean, email:boolean}) => {
    const contactMethods = []
    if (sms) {
      contactMethods.push('sms')
    }
    if (email) {
      contactMethods.push('email')
    }
    const subscriberResponse = await registerSubscriber({contact_methods: contactMethods})
    if (subscriberResponse === null) {
      console.error("Failed to register subscriber. Please try again later.")
    }
    promptForContactMethods(false);
  }      

    return (
    <Modal overlayProps={{ backgroundOpacity: 0.55, blur: 3 }} centered closeOnClickOutside={false} closeOnEscape={false} classNames={{content: classes.root, header:classes.modalHeader, title: classes.modalTitle, body:classes.modalBody, close: classes.closeButton}} opened={true} onClose={close} title="Contact Methods">
        <Space h="md"></Space>
        <Text className={classes.modalText}>Hey {name}, how can we contact you with labour updates for people you are subscribed to?</Text>
        <Space h="md"></Space>
        <Checkbox classNames={{label: classes.checkBoxLabelText}} variant="outline" defaultChecked label="Email" radius="lg" size="md" onChange={(event) => setEmail(event.currentTarget.checked)} />
        <Space h="md"></Space>
        <Checkbox classNames={{label: classes.checkBoxLabelText}} variant="outline" defaultChecked label="Text Message" radius="lg" size="md" onChange={(event) => setSMS(event.currentTarget.checked)}/>
        <Space h="xl"></Space>
        <Group justify='flex-end'>
            <Button radius="lg" onClick={() => contactMethodsDialogSubmitted({sms, email})}>Submit</Button>
        </Group>
    </Modal>
    )
}