import { Button, PinInput, Space, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useAuth } from 'react-oidc-context';
import { OpenAPI, SubscriberService, SubscribeToRequest } from '../../../client';
import { useNavigate } from 'react-router-dom';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import ContactMethodsModal from '../../../shared-components/ContactMethodsModal/ContactMethodsModal';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';

export default function SubscribeForm({ birthingPersonId, newUser, setNewUser }: { birthingPersonId: string, newUser: boolean, setNewUser: Function }) {
    const auth = useAuth()
    const navigate = useNavigate();
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            token: '',
        },
        validate: {
            token: (value) => (value.length !== 8 ? 'Invalid token': null),
        },
    });

    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }
    
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: async (values: typeof form.values) => {
            const requestBody: SubscribeToRequest = { "token": values.token }
            const response = await SubscriberService.subscribeToApiV1SubscriberSubscribeToBirthingPersonIdPost(
                {requestBody:requestBody, birthingPersonId:birthingPersonId}
            )
            return response.subscriber
        },
        onSuccess: (subscriber) => {
          queryClient.setQueryData(['subscriber', auth.user?.profile.sub], subscriber);
          navigate("/");
        },
        onError: (_) => {
            // TODO error message depends on http status of response
            notifications.show(
                {
                    title: 'Error',
                    message: 'Invalid or incorrect token',
                    radius: "lg",
                    color: "var(--mantine-color-pink-9)",
                    classNames: {
                        title: baseClasses.notificationTitle,
                        description: baseClasses.notificationDescription,
                    },
                    style:{ backgroundColor: "var(--mantine-color-pink-4)", color: "var(--mantine-color-white)" }
                }
            );
        }
    });

    if (newUser) {
        return (
            <ContactMethodsModal promptForContactMethods={setNewUser}></ContactMethodsModal>
        )
    } else {
        return (
            <div className={baseClasses.root}>
                <div className={baseClasses.header}>
                    <div className={baseClasses.title}>Subscribe</div>
                </div>
                <div className={baseClasses.body}>
                    <Title className={baseClasses.text}>Enter token to subscribe:</Title>
                    <Space h="xl"></Space>
                    <form onSubmit={form.onSubmit(() => mutation.mutate(form.values))}>
                        <PinInput
                            fw={600}
                            size='lg'
                            length={8}
                            radius="md"
                            key={form.key('token')}
                            {...form.getInputProps('token')}
                        />
                    <Space h="xl"></Space>
                    <div className={baseClasses.flexRowEnd}>
                        <Button color='var(--mantine-color-pink-4)' size='lg' radius='lg' variant='filled' type="submit">Submit</Button>
                    </div>
                    </form>
                </div>
            </div>
        );
    }
}