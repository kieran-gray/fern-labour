import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { BeginLabourRequest, LabourResponse } from '../../../client';

export default function BeginLabourButton({setLabour}: {setLabour: Function}) {
    const auth = useAuth()
    const beginLabour = async () => {
        try {
            const headers = {
                'Authorization': `Bearer ${auth.user?.access_token}`,
                'Content-Type': 'application/json'
            }
            const requestBody: BeginLabourRequest = {
                "first_labour": true
            }
            const response = await fetch(
                'http://localhost:8000/api/v1/labour/begin',
                { method: 'POST', headers: headers, body: JSON.stringify(requestBody) }
            );
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data: LabourResponse = await response.json();
            setLabour(data.labour)
        } catch (err) {
            console.error('Error starting labour:', err);
        }
    }
    return <Button size="lg" radius="lg" color='var(--mantine-color-pink-4)' variant="filled" onClick={beginLabour}>Begin Labour</Button>;
}