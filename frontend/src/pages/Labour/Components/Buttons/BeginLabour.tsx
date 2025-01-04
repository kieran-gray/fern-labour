import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { BeginLabourRequest, LabourService, OpenAPI } from '../../../../client';

export default function BeginLabourButton({setLabour}: {setLabour: Function}) {
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }

    const beginLabour = async () => {
        try {
            const requestBody: BeginLabourRequest = {
                "first_labour": true
            }
            const response = await LabourService.beginLabourApiV1LabourBeginPost(
                {requestBody: requestBody}
            )
            setLabour(response.labour)
        } catch (err) {
            console.error('Error starting labour:', err);
        }
    }
    return <Button size="lg" radius="lg" color='var(--mantine-color-pink-4)' variant="filled" onClick={beginLabour}>Begin Labour</Button>;
}