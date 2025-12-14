/**
 * V2 Labour Data Hooks
 * Uses the new Cloudflare Workers API with CQRS pattern
 */

import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import type {
  LabourServiceV2Client,
  Cursor,
  LabourUpdateType,
} from '@clients/labour_service_v2';
import { useApiAuth } from '../useApiAuth';
import { NotFoundError } from '@base/lib/errors';

// Query Keys for V2
export const queryKeysV2 = {
  labour: {
    all: ['labour-v2'] as const,
    byId: (labourId: string) => [...queryKeysV2.labour.all, labourId] as const,
    history: (userId: string) => [...queryKeysV2.labour.all, 'history', userId] as const,
    active: (userId: string) => [...queryKeysV2.labour.all, 'active', userId] as const,
  },
  contractions: {
    all: ['contractions-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.contractions.all, labourId] as const,
    paginated: (labourId: string, cursor: string | null) =>
      [...queryKeysV2.contractions.byLabour(labourId), 'paginated', cursor] as const,
    byId: (labourId: string, contractionId: string) =>
      [...queryKeysV2.contractions.byLabour(labourId), contractionId] as const,
  },
  labourUpdates: {
    all: ['labour-updates-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.labourUpdates.all, labourId] as const,
    paginated: (labourId: string, cursor: string | null) =>
      [...queryKeysV2.labourUpdates.byLabour(labourId), 'paginated', cursor] as const,
    byId: (labourId: string, labourUpdateId: string) =>
      [...queryKeysV2.labourUpdates.byLabour(labourId), labourUpdateId] as const,
  },
  subscriptionToken: {
    all: ['subscription-token-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.subscriptionToken.all, labourId] as const,
  },
} as const;

// Helper function to decode cursor
function decodeCursor(cursorString: string): Cursor {
  try {
    const decoded = atob(cursorString);
    const [updatedAt, id] = decoded.split('|');
    return { id, updated_at: updatedAt };
  } catch {
    throw new Error('Invalid cursor format');
  }
}

/**
 * Hook to get labour by ID or active
 * Always returns full LabourReadModel
 */
export function useCurrentLabourV2(client: LabourServiceV2Client, labourId: string | null) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: labourId
      ? queryKeysV2.labour.byId(labourId)
      : queryKeysV2.labour.active(user?.sub || ''),
    queryFn: async () => {
      let targetLabourId = labourId;

      if (!targetLabourId) {
        const activeResponse = await client.getActiveLabour();

        if (!activeResponse.success) {
          throw new Error(activeResponse.error || 'Failed to load active labour');
        }

        if (!activeResponse.data) {
          throw new NotFoundError;
        }

        targetLabourId = activeResponse.data.labour_id;
      }

      const response = await client.getLabour(targetLabourId);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load labour');
      }

      return response.data;
    },
    enabled: !!user?.sub,
    retry: 0,
  });
}

/**
 * Hook to get labour by ID
 */
export function useLabourByIdV2(client: LabourServiceV2Client, labourId: string | null) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: labourId ? queryKeysV2.labour.byId(labourId) : [],
    queryFn: async () => {
      if (!labourId) {
        throw new Error('Labour ID is required');
      }

      const response = await client.getLabour(labourId);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load labour');
      }

      return response.data;
    },
    enabled: !!labourId && !!user?.sub,
    retry: 0,
  });
}

/**
 * Hook to get labour history
 */
export function useLabourHistoryV2(client: LabourServiceV2Client) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeysV2.labour.history(user?.sub || ''),
    queryFn: async () => {
      const response = await client.getLabourHistory();

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load labour history');
      }

      return response.data;
    },
    enabled: !!user?.sub,
    retry: 0,
  });
}

/**
 * Hook to get active labour
 */
export function useActiveLabourV2(client: LabourServiceV2Client) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeysV2.labour.active(user?.sub || ''),
    queryFn: async () => {
      const response = await client.getActiveLabour();

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load active labour');
      }

      return response.data;
    },
    enabled: !!user?.sub,
    retry: 0,
  });
}

/**
 * Hook to get paginated contractions
 */
export function useContractionsV2(
  client: LabourServiceV2Client,
  labourId: string | null,
  limit: number = 20,
  cursor: string | null = null
) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: labourId ? queryKeysV2.contractions.paginated(labourId, cursor) : [],
    queryFn: async () => {
      if (!labourId) {
        throw new Error('Labour ID is required');
      }

      const decodedCursor = cursor ? decodeCursor(cursor) : undefined;
      const response = await client.getContractions(labourId, limit, decodedCursor);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load contractions');
      }

      return response.data;
    },
    enabled: !!labourId && !!user?.sub,
    retry: 0,
  });
}

/**
 * Hook to get a single contraction by ID
 */
export function useContractionByIdV2(
  client: LabourServiceV2Client,
  labourId: string | null,
  contractionId: string | null
) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey:
      labourId && contractionId ? queryKeysV2.contractions.byId(labourId, contractionId) : [],
    queryFn: async () => {
      if (!labourId || !contractionId) {
        throw new Error('Labour ID and Contraction ID are required');
      }

      const response = await client.getContractionById(labourId, contractionId);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load contraction');
      }

      return response.data.data[0] || null;
    },
    enabled: !!labourId && !!contractionId && !!user?.sub,
    retry: 0,
  });
}

/**
 * Hook to get paginated labour updates
 */
export function useLabourUpdatesV2(
  client: LabourServiceV2Client,
  labourId: string | null,
  limit: number = 20,
  cursor: string | null = null
) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: labourId ? queryKeysV2.labourUpdates.paginated(labourId, cursor) : [],
    queryFn: async () => {
      if (!labourId) {
        throw new Error('Labour ID is required');
      }

      const decodedCursor = cursor ? decodeCursor(cursor) : undefined;
      const response = await client.getLabourUpdates(labourId, limit, decodedCursor);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load labour updates');
      }

      return response.data;
    },
    enabled: !!labourId && !!user?.sub,
    retry: 0,
  });
}

/**
 * Hook to get a single labour update by ID
 */
export function useLabourUpdateByIdV2(
  client: LabourServiceV2Client,
  labourId: string | null,
  labourUpdateId: string | null
) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey:
      labourId && labourUpdateId
        ? queryKeysV2.labourUpdates.byId(labourId, labourUpdateId)
        : [],
    queryFn: async () => {
      if (!labourId || !labourUpdateId) {
        throw new Error('Labour ID and Labour Update ID are required');
      }

      const response = await client.getLabourUpdateById(labourId, labourUpdateId);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load labour update');
      }

      return response.data.data[0] || null;
    },
    enabled: !!labourId && !!labourUpdateId && !!user?.sub,
    retry: 0,
  });
}

// Mutation Hooks

/**
 * Hook for starting a contraction
 */
export function useStartContractionV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ labourId, startTime }: { labourId: string; startTime: Date }) => {
      const response = await client.startContraction(labourId, startTime);

      if (!response.success) {
        throw new Error(response.error || 'Failed to start contraction');
      }

      return response.data;
    },
    onSuccess: (_, __) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.contractions.all,
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to start contraction: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for ending a contraction
 */
export function useEndContractionV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      labourId,
      endTime,
      intensity,
    }: {
      labourId: string;
      endTime: Date;
      intensity: number;
    }) => {
      const response = await client.endContraction(labourId, endTime, intensity);

      if (!response.success) {
        throw new Error(response.error || 'Failed to end contraction');
      }

      return response.data;
    },
    onSuccess: (_, __) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.contractions.all,
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to end contraction: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for updating a contraction
 */
export function useUpdateContractionV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: {
      labourId: string;
      contractionId: string;
      startTime?: Date;
      endTime?: Date;
      intensity?: number;
    }) => {
      const response = await client.updateContraction(params);

      if (!response.success) {
        throw new Error(response.error || 'Failed to update contraction');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.contractions.byLabour(variables.labourId),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Contraction updated',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to update contraction: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for deleting a contraction
 */
export function useDeleteContractionV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      labourId,
      contractionId,
    }: {
      labourId: string;
      contractionId: string;
    }) => {
      const response = await client.deleteContraction(labourId, contractionId);

      if (!response.success) {
        throw new Error(response.error || 'Failed to delete contraction');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.contractions.byLabour(variables.labourId),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Contraction deleted',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to delete contraction: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for updating a labour update message
 */
export function useUpdateLabourUpdateMessageV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      labourId,
      labourUpdateId,
      message,
    }: {
      labourId: string;
      labourUpdateId: string;
      message: string;
    }) => {
      const response = await client.updateLabourUpdateMessage(labourId, labourUpdateId, message);

      if (!response.success) {
        throw new Error(response.error || 'Failed to update labour update type');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labourUpdates.byLabour(variables.labourId),
      });

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
  });
}

/**
 * Hook for updating a labour update type
 */
export function useUpdateLabourUpdateTypeV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      labourId,
      labourUpdateId,
      labourUpdateType,
    }: {
      labourId: string;
      labourUpdateId: string;
      labourUpdateType: LabourUpdateType;
    }) => {
      const response = await client.updateLabourUpdateType(labourId, labourUpdateId, labourUpdateType);

      if (!response.success) {
        throw new Error(response.error || 'Failed to update labour update type');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labourUpdates.byLabour(variables.labourId),
      });

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
  });
}

/**
 * Hook for posting a labour update
 */
export function usePostLabourUpdateV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      labourId,
      updateType,
      message,
    }: {
      labourId: string;
      updateType: LabourUpdateType;
      message: string;
    }) => {
      const response = await client.postLabourUpdate(labourId, updateType, message);

      if (!response.success) {
        throw new Error(response.error || 'Failed to post labour update');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labourUpdates.byLabour(variables.labourId),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Update posted successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to post update: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for deleting a labour update
 */
export function useDeleteLabourUpdateV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      labourId,
      labourUpdateId,
    }: {
      labourId: string;
      labourUpdateId: string;
    }) => {
      const response = await client.deleteLabourUpdate(labourId, labourUpdateId);

      if (!response.success) {
        throw new Error(response.error || 'Failed to delete labour update');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labourUpdates.byLabour(variables.labourId),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Update deleted successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to delete update: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for planning a new labour
 */
export function usePlanLabourV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      firstLabour,
      dueDate,
      labourName,
    }: {
      firstLabour: boolean;
      dueDate: Date;
      labourName?: string;
    }) => {
      const response = await client.planLabour({
        firstLabour,
        dueDate,
        labourName,
      });

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to plan labour');
      }

      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labour.all,
      });

      if (data.labour_id) {
        queryClient.invalidateQueries({
          queryKey: queryKeysV2.labour.byId(data.labour_id),
        });
      }

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Labour planned successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to plan labour: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for updating labour plan
 */
export function useUpdateLabourPlanV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      labourId,
      firstLabour,
      dueDate,
      labourName,
    }: {
      labourId: string;
      firstLabour: boolean;
      dueDate: Date;
      labourName?: string;
    }) => {
      const response = await client.updateLabourPlan({
        labourId,
        firstLabour,
        dueDate,
        labourName,
      });

      if (!response.success) {
        throw new Error(response.error || 'Failed to update labour plan');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labour.byId(variables.labourId),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Labour plan updated successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to update labour plan: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for beginning labour
 */
export function useBeginLabourV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (labourId: string) => {
      const response = await client.beginLabour(labourId);

      if (!response.success) {
        throw new Error(response.error || 'Failed to begin labour');
      }

      return response.data;
    },
    onSuccess: (_, labourId) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labour.byId(labourId),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Labour has begun',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to begin labour: ${error.message}`,
      });
    },
  });
}

/**
 * Hook for completing labour
 */
export function useCompleteLabourV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({labourId, notes}: {labourId: string, notes: string}) => {
      const response = await client.completeLabour({labourId, notes});

      if (!response.success) {
        throw new Error(response.error || 'Failed to complete labour');
      }

      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labour.byId(variables.labourId),
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
 * Hook for deleting labour
 */
export function useDeleteLabourV2(client: LabourServiceV2Client) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (labourId: string) => {
      const response = await client.deleteLabour(labourId);

      if (!response.success) {
        throw new Error(response.error || 'Failed to delete labour');
      }

      return response.data;
    },
    onSuccess: (_, labourId) => {
      // Remove from cache
      queryClient.removeQueries({
        queryKey: queryKeysV2.labour.byId(labourId),
      });

      // Invalidate all labour queries
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labour.all,
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Labour deleted successfully',
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
 * Hook for fetching subscription token
 */
export function useSubscriptionTokenV2(client: LabourServiceV2Client, labourId: string | null) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: labourId ? queryKeysV2.subscriptionToken.byLabour(labourId) : [],
    queryFn: async () => {
      if (!labourId) {
        throw new Error('Labour ID is required');
      }

      const response = await client.getSubscriptionToken(labourId);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to load subscription token');
      }

      return response.data.token;
    },
    enabled: !!labourId && !!user?.sub,
    retry: 0,
  });
}
