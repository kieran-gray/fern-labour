import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { LabourService, OpenAPI, StartContractionRequest } from '../../../../client';
import { StopwatchHandle } from '../Stopwatch/Stopwatch';
import { RefObject } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';

export default function StartContractionButton(
    {stopwatchRef}: {stopwatchRef: RefObject<StopwatchHandle>}
) {
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: async () => {
            stopwatchRef.current?.start()
            const requestBody: StartContractionRequest = {
                "start_time": new Date().toISOString(),
            }
            const response = await LabourService.startContractionApiV1LabourContractionStartPost(
                {requestBody: requestBody}
            )
            return response.labour
        },
        onSuccess: (labour) => {
          queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
        },
        onError: (error) => {
          console.error("Error starting contraction", error)
        }
    });
    
    return <Button radius="lg" size='xl' variant="outline" onClick={() => mutation.mutate()}>
        Start Contraction
    </Button>;
}