import { RefObject, useState } from 'react';
import {
  ContractionDTO,
  ContractionsService,
  LabourDTO,
  StartContractionRequest,
} from '@clients/labour_service';
import { useLabour } from '@labour/LabourContext';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { Error } from '@shared/Notifications';
import { IconHourglassLow } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { StopwatchHandle } from './Stopwatch/Stopwatch';

export default function StartContractionButton({
  stopwatchRef,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
}) {
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const { user } = useApiAuth();
  const { labourId } = useLabour();
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
      await queryClient.cancelQueries({ queryKey: ['labour', user?.profile.sub] });
      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData([
        'labour',
        user?.profile.sub,
      ]);
      if (previousLabourState != null) {
        const newLabourState = _.cloneDeep(previousLabourState);
        newLabourState.contractions.push(contraction);
        queryClient.setQueryData(['labour', user?.profile.sub], newLabourState);
      }
      return { previousLabourState };
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', user?.profile.sub], labour);
    },
    onError: (error, _, context) => {
      if (context != null) {
        queryClient.setQueryData(['labour', user?.profile.sub], context.previousLabourState);
      }
      notifications.show({
        ...Error,
        title: 'Error',
        message: `Error starting contraction: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', user?.profile.sub] });
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
      color="var(--mantine-primary-color-4)"
      onClick={() => mutation.mutate(createNewContraction())}
    >
      Start Contraction
    </Button>
  );
}
