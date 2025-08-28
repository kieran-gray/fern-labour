import {
  ContractionDTO,
  ContractionsService,
  DeleteContractionRequest,
  EndContractionRequest,
  LabourDTO,
  StartContractionRequest,
  UpdateContractionRequest,
} from '@clients/labour_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { notifications } from '@mantine/notifications';
import { contractionDurationSeconds } from '../utils';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for starting a contraction
 * Includes optimistic updates for better UX
 */
export function useStartContraction() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (contraction: ContractionDTO) => {
      const requestBody: StartContractionRequest = {
        start_time: contraction.start_time,
      };
      const response = await ContractionsService.startContraction({ requestBody });
      return response.labour;
    },
    onMutate: async (contraction: ContractionDTO) => {
      await queryClient.cancelQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData(
        queryKeys.labour.user(user?.profile.sub || '')
      );
      if (previousLabourState != null) {
        const newLabourState = _.cloneDeep(previousLabourState);
        newLabourState.contractions.push(contraction);
        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), newLabourState);
      }
      return { previousLabourState };
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
    },
    onError: (error: Error, _, context) => {
      if (context?.previousLabourState) {
        queryClient.setQueryData(
          queryKeys.labour.user(user?.profile.sub || ''),
          context.previousLabourState
        );
      }
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Error starting contraction: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
    },
  });
}

/**
 * Custom hook for ending a contraction
 * Includes optimistic updates for better UX
 */
export function useEndContraction() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ intensity, endTime }: { intensity: number; endTime: string }) => {
      const requestBody: EndContractionRequest = { intensity, end_time: endTime };
      const response = await ContractionsService.endContraction({ requestBody });
      return response.labour;
    },
    onMutate: async ({ intensity, endTime }: { intensity: number; endTime: string }) => {
      await queryClient.cancelQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });

      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData(
        queryKeys.labour.user(user?.profile.sub || '')
      );

      if (previousLabourState) {
        const newLabourState = _.cloneDeep(previousLabourState);
        const activeContractionIndex = newLabourState.contractions.findIndex(
          (contraction) => contraction.is_active
        );

        if (activeContractionIndex !== -1) {
          const activeContraction = newLabourState.contractions[activeContractionIndex];
          activeContraction.end_time = endTime;
          activeContraction.intensity = intensity;
          activeContraction.is_active = false;
          activeContraction.duration = contractionDurationSeconds(activeContraction);
        }

        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), newLabourState);
      }

      return { previousLabourState };
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
    },
    onError: (error: Error, _, context) => {
      if (context?.previousLabourState) {
        queryClient.setQueryData(
          queryKeys.labour.user(user?.profile.sub || ''),
          context.previousLabourState
        );
      }
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Error ending contraction: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
    },
  });
}

/**
 * Custom hook for updating a contraction
 */
export function useUpdateContraction() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (request: UpdateContractionRequest) => {
      const response = await ContractionsService.updateContraction({
        requestBody: request,
      });
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Contraction updated successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Error updating contraction: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
    },
  });
}

/**
 * Custom hook for deleting a contraction
 */
export function useDeleteContraction() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (contractionId: string) => {
      const requestBody: DeleteContractionRequest = { contraction_id: contractionId };
      const response = await ContractionsService.deleteContraction({ requestBody });
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Contraction deleted successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Error deleting contraction: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
    },
  });
}
