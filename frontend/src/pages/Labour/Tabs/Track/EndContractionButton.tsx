import { useState } from 'react';
import { IconHourglassHigh } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { useAuth } from 'react-oidc-context';
import { Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  ContractionDTO,
  EndContractionRequest,
  LabourDTO,
  LabourService,
  OpenAPI,
} from '../../../../client';
import { contractionDurationSeconds } from '../../../../shared-components/utils';

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
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async ({ intensity, endTime }: { intensity: number; endTime: string }) => {
      setMutationInProgress(true);
      const requestBody: EndContractionRequest = { end_time: endTime, intensity };
      const response = await LabourService.endContractionApiV1LabourContractionEndPut({
        requestBody,
      });
      return response.labour;
    },
    onMutate: async ({ intensity, endTime }: { intensity: number; endTime: string }) => {
      await queryClient.cancelQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData([
        'labour',
        auth.user?.profile.sub,
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
        message: `Error ending contraction: ${error.message}`,
        radius: 'lg',
        color: 'var(--mantine-color-pink-6)',
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
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
