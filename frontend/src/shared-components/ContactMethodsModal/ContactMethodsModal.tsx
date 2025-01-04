
import { useState } from "react";
import { SubscriberDTO, RegisterSubscriberRequest, OpenAPI, SubscriberService } from "../../client";
import { useAuth } from "react-oidc-context";
import { Text, Modal, Space, Button, Group, Checkbox } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from './ContactMethodsModal.module.css';


export default function ContactMethodsModal({ name, promptForContactMethods }: { name: string, promptForContactMethods: Function }) {
  const [email, setEmail] = useState(true);
  const [sms, setSMS] = useState(true);
  const [_, { close }] = useDisclosure(false);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || ""
  }

  const registerSubscriber = async (body: RegisterSubscriberRequest): Promise<SubscriberDTO | null> => {
    try {
      const response = await SubscriberService.registerApiV1SubscriberRegisterPost({requestBody: body})
      return response.subscriber 
    } catch (err) {
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