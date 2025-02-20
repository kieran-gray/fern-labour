import { RefObject } from 'react';
import { IconHourglassLow } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button } from '@mantine/core';
import { LabourService, OpenAPI, StartContractionRequest } from '../../../../client';
import { StopwatchHandle } from './Stopwatch/Stopwatch';

export default function StartContractionButton({
  stopwatchRef,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
}) {
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async () => {
      stopwatchRef.current?.start();
      const requestBody: StartContractionRequest = {
        start_time: new Date().toISOString(),
      };
      const response = await LabourService.startContractionApiV1LabourContractionStartPost({
        requestBody,
      });
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
    },
    onError: (error) => {
      console.error('Error starting contraction', error);
    },
  });

  const icon = <IconHourglassLow size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="outline"
      onClick={() => mutation.mutate()}
    >
      Start Contraction
    </Button>
  );
}
