
import { useState } from "react";
import { OpenAPI, RegisterSubscriberRequest, SubscriberService } from "../../client";
import { useAuth } from "react-oidc-context";
import { Text, Modal, Space, Button, Group, Checkbox } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from './ContactMethodsModal.module.css';
import { useMutation, useQueryClient } from "@tanstack/react-query";


export default function ContactMethodsModal({ promptForContactMethods }: { promptForContactMethods: Function }) {
  const [email, setEmail] = useState(true);
  const [sms, setSMS] = useState(true);
  const [_, { close }] = useDisclosure(false);
  const queryClient = useQueryClient();
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || ""
  }

  const mutation = useMutation({
    mutationFn: (data: RegisterSubscriberRequest) => {
      return SubscriberService.registerApiV1SubscriberRegisterPost({requestBody: data}).then(response => response.subscriber)
    },
    onSuccess: (subscriber) => {
      queryClient.setQueryData(['subscriber', auth.user?.profile.sub], subscriber);
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] })
      promptForContactMethods(false);
    },
    onError: () => {
      console.error("Failed to register subscriber. Please try again later.")
    }
  });

  const contactMethodsDialogSubmitted = async ({sms, email}: {sms: boolean, email:boolean}) => {
    const contactMethods = []
    if (sms) {
      contactMethods.push('sms')
    }
    if (email) {
      contactMethods.push('email')
    }
    mutation.mutate({contact_methods: contactMethods})
  }      

    return (
    <Modal overlayProps={{ backgroundOpacity: 0.55, blur: 3 }} centered closeOnClickOutside={false} closeOnEscape={false} classNames={{content: classes.root, header:classes.modalHeader, title: classes.modalTitle, body:classes.modalBody, close: classes.closeButton}} opened={true} onClose={close} title="Contact Methods">
        <Space h="md"></Space>
        <Text className={classes.modalText}>Hey, how can we contact you with labour updates for people you are subscribed to?</Text>
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