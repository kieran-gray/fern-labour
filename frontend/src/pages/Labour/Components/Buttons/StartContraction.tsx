import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { LabourService, OpenAPI, StartContractionRequest } from '../../../../client';
import { StopwatchHandle } from '../Stopwatch/Stopwatch';
import { RefObject } from 'react';

export default function StartContractionButton(
    {setLabour, stopwatchRef}: {setLabour: Function, stopwatchRef: RefObject<StopwatchHandle>}
) {
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }
    
    const startContraction = async () => {
        stopwatchRef.current?.start()
        try {
            const requestBody: StartContractionRequest = {
                "start_time": new Date().toISOString()
            }
            const response = await LabourService.startContractionApiV1LabourContractionStartPost(
                {requestBody: requestBody}
            )
            setLabour(response.labour)
        } catch (err) {
            console.error('Error starting contraction:', err);
        }
    }
    return <Button radius="lg" size='xl' variant="outline" onClick={startContraction}>Start Contraction</Button>;
}