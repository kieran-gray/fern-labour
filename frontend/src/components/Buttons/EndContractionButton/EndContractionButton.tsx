import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { EndContractionRequest, LabourResponse } from '../../../client';

export default function EndContractionButton({setLabour}: {setLabour: Function}) {
    const auth = useAuth()
    const endContraction = async () => {
        try {
            const headers = {
                'Authorization': `Bearer ${auth.user?.access_token}`,
                'Content-Type': 'application/json'
            }
            const requestBody: EndContractionRequest = {
                "end_time": new Date().toISOString(),
                "intensity": 5,
                "notes": null
            }
            const response = await fetch(
                'http://localhost:8000/api/v1/labour/contraction/end',
                { method: 'PUT', headers: headers, body: JSON.stringify(requestBody) }
            );
            if (!response.ok) {
                console.log(response)
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data: LabourResponse = await response.json();
            setLabour(data.labour)
        } catch (err) {
            console.error('Error starting contraction:', err);
        }
    }
    return <Button size='xl' variant="light" onClick={endContraction}>End Contraction</Button>;
}