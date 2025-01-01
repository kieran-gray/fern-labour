import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { CompleteLabourRequest, LabourResponse } from '../../../client';

export default function CompleteLabourButton({setLabour}: {setLabour: Function}) {
    const auth = useAuth()
    const completeLabour = async () => {
        try {
            const headers = {
                'Authorization': `Bearer ${auth.user?.access_token}`,
                'Content-Type': 'application/json'
            }
            const requestBody: CompleteLabourRequest = {
                "end_time": new Date().toISOString(),
                "notes": "test from frontend"
            }
            const response = await fetch(
                'http://localhost:8000/api/v1/labour/complete',
                { method: 'PUT', headers: headers, body: JSON.stringify(requestBody) }
            );
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data: LabourResponse = await response.json();
            setLabour(data.labour)
        } catch (err) {
            console.error('Error starting contraction:', err);
        }
    }
    return <Button variant="filled" onClick={completeLabour}>Complete Labour</Button>;
}