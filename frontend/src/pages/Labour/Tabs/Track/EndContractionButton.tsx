import { useState } from 'react';
import {
  ContractionDTO,
  ContractionsService,
  EndContractionRequest,
  LabourDTO,
} from '@clients/labour_service';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { Error } from '@shared/Notifications';
import { contractionDurationSeconds } from '@shared/utils';
import { IconHourglassHigh } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';

export default function EndContractionButton({
  intensity,
  activeContraction,
  disabled,
}: {
  intensity: number;
  activeContraction: ContractionDTO;
  disabled: boolean;
}) {
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const { user } = useApiAuth();

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async ({ intensity, endTime }: { intensity: number; endTime: string }) => {
      setMutationInProgress(true);
      const requestBody: EndContractionRequest = { end_time: endTime, intensity };
      const response = await ContractionsService.endContraction({ requestBody });
      return response.labour;
    },
    onMutate: async ({ intensity, endTime }: { intensity: number; endTime: string }) => {
      await queryClient.cancelQueries({ queryKey: ['labour', user?.profile.sub] });
      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData([
        'labour',
        user?.profile.sub,
      ]);
      if (previousLabourState != null) {
        const newLabourState = _.cloneDeep(previousLabourState);

        const contraction = newLabourState.contractions.find(
          (contraction) => contraction.id === activeContraction.id
        )!;
        contraction.is_active = false;
        contraction.intensity = intensity;
        contraction.end_time = endTime;
        contraction.duration = contractionDurationSeconds(contraction);
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
        message: `Error ending contraction: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', user?.profile.sub] });
      setMutationInProgress(false);
    },
  });

  const icon = <IconHourglassHigh size={25} />;

  return (
    <Button
      leftSection={icon}
      radius="xl"
      size="xl"
      variant="white"
      loading={mutationInProgress}
      onClick={() => {
        const endTime = new Date().toISOString();
        mutation.mutate({ intensity, endTime });
      }}
      disabled={disabled}
    >
      End Contraction
    </Button>
  );
}
