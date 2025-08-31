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
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { useGuestMode } from '../../offline/hooks/useGuestMode';
import { useOfflineMutation, useOnlineMutation } from '../../offline/hooks/useOfflineMutation';
import { GuestProfileManager } from '../../offline/storage/guestProfile';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for fetching active labour data
 * Supports both authenticated and guest modes
 */
export function useActiveLabour() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();

  return useQuery({
    queryKey: isGuestMode
      ? ['labour', 'guest', guestProfile?.guestId, 'active']
      : queryKeys.labour.active(user?.profile.sub || ''),
    queryFn: async () => {
      if (isGuestMode && guestProfile) {
        const labours = await GuestProfileManager.getGuestLabours(guestProfile.guestId);
        const activeLabour = labours.find((labour) => labour.current_phase !== 'completed');
        return activeLabour || undefined;
      }
      const response = await LabourQueriesService.getActiveLabour();
      return response.labour;
    },
    enabled: !!user?.profile.sub || (isGuestMode && !!guestProfile),
    retry: 0,
  });
}

/**
 * Custom hook for fetching labour by ID
 * Supports both authenticated and guest modes
 */
export function useLabourById(labourId: string | null) {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();

  return useQuery({
    queryKey: labourId
      ? isGuestMode
        ? ['labour', 'guest', guestProfile?.guestId, 'byId', labourId]
        : queryKeys.labour.byId(labourId)
      : [],
    queryFn: async () => {
      if (!labourId) {
        throw new Error('Labour ID is required');
      }

      if (isGuestMode && guestProfile) {
        const labour = await GuestProfileManager.getGuestLabour(guestProfile.guestId, labourId);
        if (!labour) {
          throw new NotFoundError();
        }
        return labour;
      }
      try {
        const response = await LabourQueriesService.getLabourById({ labourId });
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
    enabled: !!labourId && (!!user?.profile.sub || (isGuestMode && !!guestProfile)),
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
 * Supports offline queueing and guest mode
 */
export function usePlanLabour() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();
  const queryClient = useQueryClient();

  return useOfflineMutation({
    eventType: 'plan_labour',
    getAggregateId: () => {
      return isGuestMode ? `guest-labour-${Date.now()}` : `labour-${Date.now()}`;
    },
    mutationFn: async ({
      requestBody,
      existing,
    }: {
      requestBody: PlanLabourRequest;
      existing: boolean;
    }) => {
      if (isGuestMode && guestProfile) {
        const newLabour = {
          id: `guest-labour-${Date.now()}`,
          birthing_person_id: guestProfile.guestId,
          current_phase: 'planned' as const,
          due_date: requestBody.due_date,
          first_labour: requestBody.first_labour,
          labour_name: requestBody.labour_name || null,
          start_time: null,
          end_time: null,
          notes: null,
          recommendations: {},
          contractions: [],
          labour_updates: [],
        };

        if (existing) {
          await GuestProfileManager.updateGuestLabour(
            guestProfile.guestId,
            newLabour.id,
            newLabour
          );
        } else {
          await GuestProfileManager.addGuestLabour(guestProfile.guestId, newLabour);
        }

        return newLabour;
      }
      let response;
      if (existing) {
        response = await LabourService.updateLabourPlan({ requestBody });
      } else {
        response = await LabourService.planLabour({ requestBody });
      }
      return response.labour;
    },
    onSuccess: async (labour, variables) => {
      if (isGuestMode && guestProfile) {
        queryClient.invalidateQueries({ queryKey: ['labour', 'guest', guestProfile.guestId] });
      } else {
        queryClient.invalidateQueries();
        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
        queryClient.setQueryData(queryKeys.labour.active(user?.profile.sub || ''), labour);
      }

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
 * Supports offline queueing and guest mode
 */
export function useCompleteLabour() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();
  const queryClient = useQueryClient();

  return useOfflineMutation({
    eventType: 'complete_labour',
    getAggregateId: (labourId: string) => labourId,
    mutationFn: async (labourId: string, labourNotes?: string) => {
      const requestBody: CompleteLabourRequest = {
        end_time: new Date().toISOString(),
        notes: labourNotes || null,
      };

      if (isGuestMode && guestProfile) {
        await GuestProfileManager.updateGuestLabour(guestProfile.guestId, labourId, {
          current_phase: 'completed' as const,
          end_time: requestBody.end_time,
          notes: requestBody.notes,
        });
      } else {
        await LabourService.completeLabour({ requestBody });
      }
    },
    onSuccess: () => {
      if (isGuestMode && guestProfile) {
        queryClient.invalidateQueries({ queryKey: ['labour', 'guest', guestProfile.guestId] });
      } else {
        queryClient.removeQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
        queryClient.removeQueries({ queryKey: queryKeys.labour.active(user?.profile.sub || '') });
        queryClient.invalidateQueries({
          queryKey: queryKeys.labour.history(user?.profile.sub || ''),
        });
        queryClient.invalidateQueries({
          queryKey: queryKeys.birthingPerson.user(user?.profile.sub || ''),
        });
      }

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
 * Guest mode: removes from local storage
 * Authenticated: uses online mutation (no offline queueing for deletions)
 */
export function useDeleteLabour() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();
  const queryClient = useQueryClient();

  return useOnlineMutation({
    mutationFn: async (labourId: string) => {
      if (isGuestMode && guestProfile) {
        await GuestProfileManager.deleteGuestLabour(guestProfile.guestId, labourId);
      } else {
        await LabourService.deleteLabour({ labourId });
      }
    },
    onSuccess: () => {
      if (isGuestMode && guestProfile) {
        queryClient.invalidateQueries({ queryKey: ['labour', 'guest', guestProfile.guestId] });
      } else {
        queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
        queryClient.invalidateQueries({
          queryKey: queryKeys.labour.history(user?.profile.sub || ''),
        });
      }
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
 * Only available in authenticated mode (requires server API)
 */
export function useSendLabourInvite() {
  const { isGuestMode } = useGuestMode();

  return useOnlineMutation({
    mutationFn: async ({ email, labourId }: { email: string; labourId: string }) => {
      if (isGuestMode) {
        throw new Error(
          'Invites are not available in guest mode. Sign up to share your labour progress!'
        );
      }

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
