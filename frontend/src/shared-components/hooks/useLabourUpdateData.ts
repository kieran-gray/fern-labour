import {
  DeleteLabourUpdateRequest,
  LabourDTO,
  LabourUpdateDTO,
  LabourUpdateRequest,
  LabourUpdatesService,
  UpdateLabourUpdateRequest,
} from '@clients/labour_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { notifications } from '@mantine/notifications';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for creating labour updates
 * Includes optimistic updates for better UX
 */
export function useCreateLabourUpdate() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (request: LabourUpdateRequest) => {
      const response = await LabourUpdatesService.postLabourUpdate({ requestBody: request });
      return response.labour;
    },
    onMutate: async (request: LabourUpdateRequest) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });

      // Snapshot the previous value
      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData(
        queryKeys.labour.user(user?.profile.sub || '')
      );

      // Optimistically update with new labour update
      if (previousLabourState) {
        const newLabourUpdate: LabourUpdateDTO = {
          id: 'placeholder',
          labour_id: previousLabourState.id,
          labour_update_type: request.labour_update_type.toString(),
          message: request.message,
          sent_time: new Date().toISOString(),
          edited: false,
          application_generated: false,
        };

        const newLabourState = _.cloneDeep(previousLabourState);
        newLabourState.labour_updates.unshift(newLabourUpdate); // Add to beginning
        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), newLabourState);
      }

      return { previousLabourState };
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Update posted successfully',
      });
    },
    onError: (error: Error, _, context) => {
      // Rollback optimistic update
      if (context?.previousLabourState) {
        queryClient.setQueryData(
          queryKeys.labour.user(user?.profile.sub || ''),
          context.previousLabourState
        );
      }
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to post update: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
    },
  });
}

/**
 * Custom hook for editing labour updates
 */
export function useEditLabourUpdate() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (requestBody: UpdateLabourUpdateRequest) => {
      const response = await LabourUpdatesService.updateLabourUpdate({ requestBody });
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Status update edited successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to edit status update: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
    },
  });
}

/**
 * Custom hook for deleting labour updates
 */
export function useDeleteLabourUpdate() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (labourUpdateId: string) => {
      const requestBody: DeleteLabourUpdateRequest = { labour_update_id: labourUpdateId };
      const response = await LabourUpdatesService.deleteLabourUpdate({ requestBody });
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Status update deleted successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to delete status update: ${error.message}`,
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
    },
  });
}
