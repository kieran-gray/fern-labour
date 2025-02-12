import { RefObject } from 'react';
import { IconHourglassHigh } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button } from '@mantine/core';
import { EndContractionRequest, LabourService, OpenAPI } from '../../../../client';
import { StopwatchHandle } from '../Stopwatch/Stopwatch';

export default function EndContractionButton({
  intensity,
  stopwatchRef,
}: {
  intensity: number;
  stopwatchRef: RefObject<StopwatchHandle>;
}) {
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (intensity: number) => {
      const requestBody: EndContractionRequest = {
        end_time: new Date().toISOString(),
        intensity,
      };
      const response = await LabourService.endContractionApiV1LabourContractionEndPut({
        requestBody,
      });
      stopwatchRef.current?.stop();
      stopwatchRef.current?.reset();
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
    },
    onError: (error) => {
      console.error('Error ending contraction', error);
    },
  });

  const icon = <IconHourglassHigh size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="lg"
      size="xl"
      variant="white"
      onClick={() => mutation.mutate(intensity)}
    >
      End Contraction
    </Button>
  );
}
