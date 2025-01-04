import { Button, PinInput, Space, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useAuth } from 'react-oidc-context';
import { OpenAPI, SubscriberService, SubscribeToRequest } from '../../../client';
import { useNavigate } from 'react-router-dom';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import ContactMethodsModal from '../../../shared-components/ContactMethodsModal/ContactMethodsModal';

export default function SubscribeForm({ birthingPersonId, newUser, setNewUser, setError }: { birthingPersonId: string, newUser: boolean, setNewUser: Function, setError: Function }) {
    const auth = useAuth()
    const navigate = useNavigate();
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            token: '',
        },
        validate: {
            token: (value) => (/.{8}/.test(value) ? null : 'Invalid token'),
        },
    });

    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }

    const subscribeTo = async (values: typeof form.values) => {
        try {
            const requestBody: SubscribeToRequest = { "token": values.token }
            await SubscriberService.subscribeToApiV1SubscriberSubscribeToBirthingPersonIdPost(
                {requestBody:requestBody, birthingPersonId:birthingPersonId}
            )
            navigate("/")
        } catch (err) {
            // TODO error message depends on http status of response
            setError('Invalid or incorrect token');
        }
    }

    if (newUser) {
        return (
            <ContactMethodsModal name="" promptForContactMethods={setNewUser}></ContactMethodsModal>
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
                    <form onSubmit={form.onSubmit(subscribeTo)}>
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