import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { LabourResponse, StartContractionRequest } from '../../../client';

export default function StartContractionButton({setLabour}: {setLabour: Function}) {
    const auth = useAuth()
    const startContraction = async () => {
        try {
            const headers = {
                'Authorization': `Bearer ${auth.user?.access_token}`,
                'Content-Type': 'application/json'
            }
            const requestBody: StartContractionRequest = {
                "start_time": new Date().toISOString()
            }
            const response = await fetch(
                'http://localhost:8000/api/v1/labour/contraction/start',
                { method: 'POST', headers: headers, body: JSON.stringify(requestBody) }
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
    return <Button size='xl' variant="light" onClick={startContraction}>Start Contraction</Button>;
}