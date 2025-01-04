import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { EndContractionRequest, LabourService, OpenAPI } from '../../../../client';
import { StopwatchHandle } from '../Stopwatch/Stopwatch';
import { RefObject } from 'react';

export default function EndContractionButton(
    {intensity, setLabour, stopwatchRef}: {intensity: number, setLabour: Function, stopwatchRef: RefObject<StopwatchHandle>}
) {
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }

    const endContraction = async () => {
        stopwatchRef.current?.stop()
        stopwatchRef.current?.reset()
        try {
            const requestBody: EndContractionRequest = {
                "end_time": new Date().toISOString(),
                "intensity": intensity,
                "notes": null
            }
            const response = await LabourService.endContractionApiV1LabourContractionEndPut(
                {requestBody: requestBody}
            )
            setLabour(response.labour)
        } catch (err) {
            console.error('Error ending contraction:', err);
        }
    }
    return <Button radius="lg" size='xl' variant="white" onClick={endContraction}>End Contraction</Button>;
}