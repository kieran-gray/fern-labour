import { RefObject, useState } from 'react';
import { IconHourglassLow } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { useAuth } from 'react-oidc-context';
import { Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  ContractionDTO,
  ContractionsService,
  LabourDTO,
  OpenAPI,
  StartContractionRequest,
} from '../../../../client';
import { useLabour } from '../../LabourContext';
import { StopwatchHandle } from './Stopwatch/Stopwatch';

export default function StartContractionButton({
  stopwatchRef,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
}) {
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const auth = useAuth();
  const { labourId } = useLabour();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const createNewContraction = () => {
    const startTime = new Date().toISOString();
    const contraction: ContractionDTO = {
      id: 'placeholder',
      labour_id: labourId!,
      start_time: startTime,
      end_time: startTime,
      duration: 0,
      intensity: null,
      notes: null,
      is_active: true,
    };
    return contraction;
  };

  const mutation = useMutation({
    mutationFn: async (contraction: ContractionDTO) => {
      setMutationInProgress(true);
      stopwatchRef.current?.start();
      const requestBody: StartContractionRequest = {
        start_time: contraction.start_time,
      };
      const response = await ContractionsService.startContraction({ requestBody });
      return response.labour;
    },
    onMutate: async (contraction: ContractionDTO) => {
      await queryClient.cancelQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData([
        'labour',
        auth.user?.profile.sub,
      ]);
      if (previousLabourState != null) {
        const newLabourState = _.cloneDeep(previousLabourState);
        newLabourState.contractions.push(contraction);
        queryClient.setQueryData(['labour', auth.user?.profile.sub], newLabourState);
      }
      return { previousLabourState };
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
    },
    onError: (error, _, context) => {
      if (context != null) {
        queryClient.setQueryData(['labour', auth.user?.profile.sub], context.previousLabourState);
      }
      notifications.show({
        title: 'Error',
        message: `Error starting contraction: ${error.message}`,
        radius: 'lg',
        color: 'var(--mantine-color-pink-6)',
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      setMutationInProgress(false);
    },
  });

  const icon = <IconHourglassLow size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="filled"
      loading={mutationInProgress}
      color="var(--mantine-color-pink-4)"
      onClick={() => mutation.mutate(createNewContraction())}
    >
      Start Contraction
    </Button>
  );
}
