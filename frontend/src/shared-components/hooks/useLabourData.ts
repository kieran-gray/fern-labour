import { NotFoundError, PermissionDenied } from '@base/Errors';
import {
  ApiError,
  CompleteLabourRequest,
  LabourQueriesService,
  LabourService,
  PlanLabourApiV1LabourPlanPostData,
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
 * Custom hook for starting a new labour
 */
export function useStartLabour() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (request: PlanLabourApiV1LabourPlanPostData['requestBody']) => {
      const response = await LabourService.planLabour({ requestBody: request });
      return response;
    },
    onSuccess: () => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      queryClient.invalidateQueries({
        queryKey: queryKeys.labour.history(user?.profile.sub || ''),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Labour started successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to start labour: ${error.message}`,
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
      // Invalidate relevant queries
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
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
