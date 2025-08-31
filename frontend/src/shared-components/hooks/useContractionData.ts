import {
  ContractionDTO,
  ContractionsService,
  DeleteContractionRequest,
  EndContractionRequest,
  StartContractionRequest,
  UpdateContractionRequest,
} from '@clients/labour_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { useGuestMode } from '../../offline/hooks/useGuestMode';
import { useOfflineMutation } from '../../offline/hooks/useOfflineMutation';
import { GuestProfileManager } from '../../offline/storage/guestProfile';
import { contractionDurationSeconds } from '../utils';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for starting a contraction
 * Supports offline queueing and guest mode
 */
export function useStartContraction() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();
  const queryClient = useQueryClient();

  return useOfflineMutation({
    eventType: 'start_contraction',
    getAggregateId: () => {
      return isGuestMode
        ? `guest-labour-${guestProfile?.guestId || 'unknown'}`
        : `labour-${user?.profile.sub || 'unknown'}`;
    },
    mutationFn: async (requestBody: StartContractionRequest) => {
      if (isGuestMode && guestProfile) {
        const newContraction: ContractionDTO = {
          id: `contraction-${Date.now()}`,
          labour_id: `guest-labour-${guestProfile.guestId}`,
          start_time: requestBody.start_time!,
          end_time: requestBody.start_time!,
          duration: 0,
          intensity: 5,
          notes: null,
          is_active: true,
        };

        const labours = await GuestProfileManager.getGuestLabours(guestProfile.guestId);
        const labour = labours.find((l) => l.id === `guest-labour-${guestProfile.guestId}`)!;

        labour.contractions.push(newContraction);
        await GuestProfileManager.updateGuestLabour(guestProfile.guestId, labour.id, {
          contractions: labour.contractions,
        });

        return labour;
      }
      const response = await ContractionsService.startContraction({ requestBody });
      return response.labour;
    },
    onMutate: async (requestBody) => {
      if (isGuestMode) {
        return;
      }
      const sub = user?.profile.sub || '';
      const labourKey = queryKeys.labour.user(sub);
      const previous = queryClient.getQueryData(labourKey) as any;
      if (!previous) {
        return { labourKey, previous };
      }

      const optimistic: ContractionDTO = {
        id: `optimistic-${Date.now()}`,
        labour_id: previous.id,
        start_time: (requestBody as StartContractionRequest).start_time!,
        end_time: (requestBody as StartContractionRequest).start_time!,
        duration: 0,
        intensity: (requestBody as any).intensity ?? 5,
        notes: null,
        is_active: true,
      };
      const next = {
        ...previous,
        contractions: [...(previous.contractions || []), optimistic],
      };
      queryClient.setQueryData(labourKey, next);
      return { labourKey, previous };
    },
    onSuccess: (labour) => {
      if (!labour) {
        return;
      }
      if (isGuestMode && guestProfile) {
        queryClient.invalidateQueries({ queryKey: ['labour', 'guest', guestProfile.guestId] });
      } else {
        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
        queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      }
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Error starting contraction: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for ending a contraction
 * Supports offline queueing and guest mode
 */
export function useEndContraction() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();
  const queryClient = useQueryClient();

  return useOfflineMutation({
    eventType: 'end_contraction',
    getAggregateId: () => {
      return isGuestMode
        ? `guest-labour-${guestProfile?.guestId || 'unknown'}`
        : `labour-${user?.profile.sub || 'unknown'}`;
    },
    mutationFn: async ({ intensity, endTime }: { intensity: number; endTime: string }) => {
      if (isGuestMode && guestProfile) {
        const labours = await GuestProfileManager.getGuestLabours(guestProfile.guestId);
        const labour = labours.find((l) => l.id === `guest-labour-${guestProfile.guestId}`)!;

        const activeContractionIndex = labour.contractions.findIndex((c) => c.is_active);
        if (activeContractionIndex !== -1) {
          const activeContraction = labour.contractions[activeContractionIndex];
          activeContraction.end_time = endTime;
          activeContraction.intensity = intensity;
          activeContraction.is_active = false;
          activeContraction.duration = contractionDurationSeconds(activeContraction);

          await GuestProfileManager.updateGuestLabour(guestProfile.guestId, labour.id, {
            contractions: labour.contractions,
          });
        }

        return labour;
      }
      const requestBody: EndContractionRequest = { intensity, end_time: endTime };
      const response = await ContractionsService.endContraction({ requestBody });
      return response.labour;
    },
    getPayload: ({ intensity, endTime }: { intensity: number; endTime: string }) => ({
      intensity,
      end_time: endTime,
    }),
    onMutate: async (vars) => {
      if (isGuestMode) {
        return;
      }
      const sub = user?.profile.sub || '';
      const labourKey = queryKeys.labour.user(sub);
      const previous = queryClient.getQueryData(labourKey) as any;
      if (!previous) {
        return { labourKey, previous };
      }

      const next = { ...previous, contractions: [...(previous.contractions || [])] };
      const idx = next.contractions.findIndex((c: ContractionDTO) => c.is_active);
      if (idx !== -1) {
        const active = { ...next.contractions[idx] } as ContractionDTO;
        active.end_time = (vars as { endTime: string }).endTime;
        active.intensity = (vars as { intensity: number }).intensity;
        active.is_active = false;
        active.duration = contractionDurationSeconds(active);
        next.contractions[idx] = active;
        queryClient.setQueryData(labourKey, next);
      }
      return { labourKey, previous };
    },
    onSuccess: (labour) => {
      if (!labour) {
        return;
      }
      if (isGuestMode && guestProfile) {
        queryClient.invalidateQueries({ queryKey: ['labour', 'guest', guestProfile.guestId] });
      } else {
        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
        queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      }
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Error ending contraction: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for updating a contraction
 * Supports offline queueing and guest mode
 */
export function useUpdateContraction() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();
  const queryClient = useQueryClient();

  return useOfflineMutation({
    eventType: 'update_contraction',
    getAggregateId: () => {
      return isGuestMode
        ? `guest-labour-${guestProfile?.guestId || 'unknown'}`
        : `labour-${user?.profile.sub || 'unknown'}`;
    },
    mutationFn: async (request: UpdateContractionRequest) => {
      if (isGuestMode && guestProfile) {
        const labours = await GuestProfileManager.getGuestLabours(guestProfile.guestId);
        const labour = labours.find((l) => l.id === `guest-labour-${guestProfile.guestId}`)!;

        const contractionIndex = labour.contractions.findIndex(
          (c) => c.id === request.contraction_id
        );
        if (contractionIndex !== -1) {
          const contraction = labour.contractions[contractionIndex];
          if (request.intensity !== undefined) {
            contraction.intensity = request.intensity;
          }
          if (request.notes !== undefined) {
            contraction.notes = request.notes;
          }
          if (request.start_time != null) {
            contraction.start_time = request.start_time;
          }
          if (request.end_time != null) {
            contraction.end_time = request.end_time;
          }

          if (request.start_time || request.end_time) {
            contraction.duration = contractionDurationSeconds(contraction);
          }

          await GuestProfileManager.updateGuestLabour(guestProfile.guestId, labour.id, {
            contractions: labour.contractions,
          });
        }
        return labour;
      }
      const response = await ContractionsService.updateContraction({ requestBody: request });
      return response.labour;
    },
    onSuccess: (labour) => {
      if (isGuestMode && guestProfile) {
        queryClient.invalidateQueries({ queryKey: ['labour', 'guest', guestProfile.guestId] });
      } else {
        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
        queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      }

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
  });
}

/**
 * Custom hook for deleting a contraction
 * Supports offline queueing and guest mode
 */
export function useDeleteContraction() {
  const { user } = useApiAuth();
  const { isGuestMode, guestProfile } = useGuestMode();
  const queryClient = useQueryClient();

  return useOfflineMutation({
    eventType: 'delete_contraction',
    getAggregateId: () => {
      return isGuestMode
        ? `guest-labour-${guestProfile?.guestId || 'unknown'}`
        : `labour-${user?.profile.sub || 'unknown'}`;
    },
    mutationFn: async (contractionId: string) => {
      if (isGuestMode && guestProfile) {
        const labours = await GuestProfileManager.getGuestLabours(guestProfile.guestId);
        const labour = labours.find((l) => l.id === `guest-labour-${guestProfile.guestId}`);

        if (labour) {
          const contractionIndex = labour.contractions.findIndex((c) => c.id === contractionId);
          if (contractionIndex !== -1) {
            labour.contractions.splice(contractionIndex, 1);
            await GuestProfileManager.updateGuestLabour(guestProfile.guestId, labour.id, {
              contractions: labour.contractions,
            });
          }
        }

        return labour;
      }
      const requestBody: DeleteContractionRequest = { contraction_id: contractionId };
      const response = await ContractionsService.deleteContraction({ requestBody });
      return response.labour;
    },
    onSuccess: (labour) => {
      if (isGuestMode && guestProfile) {
        queryClient.invalidateQueries({ queryKey: ['labour', 'guest', guestProfile.guestId] });
      } else {
        queryClient.setQueryData(queryKeys.labour.user(user?.profile.sub || ''), labour);
        queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.profile.sub || '') });
      }

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
  });
}
