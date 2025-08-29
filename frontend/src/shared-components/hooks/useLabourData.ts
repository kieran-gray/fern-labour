import { NotFoundError, PermissionDenied } from '@base/Errors';
import {
  ApiError,
  CompleteLabourRequest,
  LabourQueriesService,
  LabourService,
  PlanLabourRequest,
  SendInviteRequest,
} from '@clients/labour_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for fetching active labour data
 */
export function useActiveLabour() {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.labour.active(user?.profile.sub || ''),
    queryFn: async () => {
      const response = await LabourQueriesService.getActiveLabour();
      return response.labour;
    },
    enabled: !!user?.profile.sub,
    retry: 0,
  });
}

/**
 * Custom hook for fetching labour by ID
 */
export function useLabourById(labourId: string | null) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: labourId ? queryKeys.labour.byId(labourId) : [],
    queryFn: async () => {
      if (!labourId) {
        throw new Error('Labour ID is required');
      }
      const response = await LabourQueriesService.getLabourById({ labourId });
      return response.labour;
    },
    enabled: !!labourId && !!user?.profile.sub,
    retry: 0,
  });
}

/**
 * Custom hook for fetching current labour (active or by ID)
 * Handles the logic of determining which labour to fetch
 */
export function useCurrentLabour(labourId?: string | null) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.labour.user(user?.profile.sub || ''),
    queryFn: async () => {
      try {
        let response;
        if (labourId) {
          response = await LabourQueriesService.getLabourById({ labourId });
        } else {
          response = await LabourQueriesService.getActiveLabour();
        }
        return response.labour;
      } catch (err) {
        if (err instanceof ApiError) {
          if (err.status === 404) {
            throw new NotFoundError();
          } else if (err.status === 403) {
            throw new PermissionDenied();
          }
        }
        throw new Error('Failed to load labour. Please try again later.');
      }
    },
    enabled: !!user?.profile.sub,
    retry: 0,
  });
}

/**
 * Custom hook for fetching labour history
 */
export function useLabourHistory() {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.labour.history(user?.profile.sub || ''),
    queryFn: async () => {
      try {
        const response = await LabourQueriesService.getAllLabours();
        return response;
      } catch (err) {
        throw new Error('Failed to load labour history. Please try again later.');
      }
    },
    enabled: !!user?.profile.sub,
  });
}

/**
 * Custom hook for planning a new labour
 */
export function usePlanLabour() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      requestBody,
      existing,
    }: {
      requestBody: PlanLabourRequest;
      existing: boolean;
    }) => {
      let response;
      if (existing) {
        response = await LabourService.updateLabourPlan({ requestBody });
      } else {
        response = await LabourService.planLabour({ requestBody });
      }
      return response.labour;
    },
    onSuccess: async (labour, variables) => {
      queryClient.invalidateQueries();

      queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
      queryClient.setQueryData(queryKeys.labour.active(user?.profile.sub || ''), labour);
      const message = variables.existing ? 'Labour Plan Updated' : 'Labour Planned';
      notifications.show({
        ...Success,
        title: 'Success',
        message,
      });
    },
    onError: () => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Something went wrong. Please try again.`,
      });
    },
  });
}

/**
 * Custom hook for completing labour
 */
export function useCompleteLabour() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (labourNotes: string) => {
      const requestBody: CompleteLabourRequest = {
        end_time: new Date().toISOString(),
        notes: labourNotes,
      };
      await LabourService.completeLabour({ requestBody });
    },
    onSuccess: () => {
      queryClient.removeQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      queryClient.removeQueries({ queryKey: queryKeys.labour.active(user?.profile.sub || '') });
      queryClient.invalidateQueries({
        queryKey: queryKeys.labour.history(user?.profile.sub || ''),
      });
      queryClient.invalidateQueries({
        queryKey: queryKeys.birthingPerson.user(user?.profile.sub || ''),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Labour completed successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to complete labour: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for deleting labour
 */
export function useDeleteLabour() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (labourId: string) => {
      await LabourService.deleteLabour({ labourId });
    },
    onSuccess: () => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      queryClient.invalidateQueries({
        queryKey: queryKeys.labour.history(user?.profile.sub || ''),
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to delete labour: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for sending labour invites
 */
export function useSendLabourInvite() {
  return useMutation({
    mutationFn: async ({ email, labourId }: { email: string; labourId: string }) => {
      const requestBody: SendInviteRequest = { invite_email: email, labour_id: labourId };
      await LabourService.sendInvite({ requestBody });
    },
    onSuccess: () => {
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Invite email sent',
      });
    },
    onError: (err) => {
      if (err instanceof ApiError && err.status === 429) {
        notifications.show({
          ...ErrorNotification,
          title: 'Slow down!',
          message: 'You have sent too many invites today. Wait until tomorrow to send more.',
        });
      } else {
        notifications.show({
          ...ErrorNotification,
          title: 'Error sending invite',
          message: 'Something went wrong. Please try again.',
        });
      }
    },
  });
}

/**
 * Custom hook for refreshing labour data when switching labours
 */
export function useRefreshLabourData() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return async () => {
    // Invalidate all labour-related queries for the current user
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') }),
      queryClient.invalidateQueries({
        queryKey: queryKeys.labour.history(user?.profile.sub || ''),
      }),
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
      }),
    ]);
  };
}
