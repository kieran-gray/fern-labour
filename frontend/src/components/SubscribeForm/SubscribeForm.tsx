import { Button, Group, PinInput, Space, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useAuth } from 'react-oidc-context';
import { SubscribeToRequest } from '../../client';
import { useNavigate } from 'react-router-dom';
import classes from './SubscribeForm.module.css';

export default function SubscribeForm({ birthingPersonId }: { birthingPersonId: string }) {
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

    const subscribeTo = async (values: typeof form.values) => {
        try {
            const headers = {
                'Authorization': `Bearer ${auth.user?.access_token}`,
                'Content-Type': 'application/json'
            }
            const requestBody: SubscribeToRequest = { "token": values.token }
            const response = await fetch(
                `http://localhost:8000/api/v1/subscriber/subscribe_to/${birthingPersonId}`,
                { method: 'POST', headers: headers, body: JSON.stringify(requestBody) }
            );
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            navigate("/")
        } catch (err) {
            console.error('Error starting labour:', err);
        }
    }

    return (
        <div className={classes.wrapper}>
            <div className={classes.body} >
                    <Title size="xl">Enter token to subscribe:</Title>
                    <Space h="xl"></Space>
                    <form onSubmit={form.onSubmit(subscribeTo)}>
                        <PinInput
                            size='lg'
                            length={6}
                            radius="md"
                            key={form.key('token')}
                            {...form.getInputProps('token')}
                        />
                    </form>
                    <Space h="xl"></Space>
                <Group justify='flex-end'>
                    <Button type="submit">Submit</Button>
                </Group>
            </div>
        </div>

    );
}