import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { EndContractionRequest, LabourService, OpenAPI } from '../../../../client';
import { StopwatchHandle } from '../Stopwatch/Stopwatch';
import { RefObject } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';

export default function EndContractionButton(
    {intensity, stopwatchRef}: {intensity: number, stopwatchRef: RefObject<StopwatchHandle>}
) {
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }
    
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: async (intensity: number) => {
            const requestBody: EndContractionRequest = {
                "end_time": new Date().toISOString(),
                "intensity": intensity,
            }
            const response = await LabourService.endContractionApiV1LabourContractionEndPut(
                {requestBody: requestBody}
            )
            stopwatchRef.current?.stop()
            stopwatchRef.current?.reset()
            return response.labour
        },
        onSuccess: (labour) => {
          queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
        },
        onError: (error) => {
          console.error("Error ending contraction", error)
        }
    });
    return <Button radius="lg" size='xl' variant="white" onClick={() => mutation.mutate(intensity)}>
        End Contraction
    </Button>;
}