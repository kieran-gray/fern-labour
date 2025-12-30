/**
 * Mutation Factory
 *
 * Reduces boilerplate for the common mutation pattern:
 * 1. Call client method
 * 2. Check response.success, throw error if not
 * 3. On success: optionally invalidate query (when WebSocket disconnected) + show notification
 * 4. On error: optionally invalidate query + show notification
 */

import type { LabourServiceClient } from '@base/clients/labour_service';
import { useWebSocket } from '@base/contexts/WebsocketContext';
import { Error as ErrorNotification, Success } from '@components/Notifications';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

interface MutationConfig<TParams, TResult> {
  mutationFn: (client: LabourServiceClient, params: TParams) => Promise<ApiResponse<TResult>>;
  getInvalidationKey?: (params: TParams) => readonly unknown[];
  invalidateOnError?: boolean;
  successMessage: string;
  errorMessage: string;
}

/**
 * Creates a mutation hook with standardized error handling and cache invalidation.
 *
 * @example
 * export const useDeleteContraction = createMutation({
 *   mutationFn: (client, { labourId, contractionId }) =>
 *     client.deleteContraction(labourId, contractionId),
 *   getInvalidationKey: ({ labourId }) => queryKeys.contractions.infinite(labourId),
 *   successMessage: 'Contraction deleted',
 *   errorMessage: 'Failed to delete contraction',
 * });
 */
export function createMutation<TParams, TResult = void>(config: MutationConfig<TParams, TResult>) {
  return function useCreatedMutation(client: LabourServiceClient) {
    const queryClient = useQueryClient();
    const { isConnected } = useWebSocket();

    return useMutation({
      mutationFn: async (params: TParams) => {
        const response = await config.mutationFn(client, params);

        if (!response.success) {
          throw new Error(response.error || config.errorMessage);
        }

        return response.data as TResult;
      },

      onSuccess: (_, params) => {
        if (!isConnected && config.getInvalidationKey) {
          queryClient.invalidateQueries({
            queryKey: config.getInvalidationKey(params),
          });
        }

        notifications.show({
          ...Success,
          title: 'Success',
          message: config.successMessage,
        });
      },

      onError: (error: Error, params) => {
        const shouldInvalidateOnError = config.invalidateOnError ?? true;

        if (shouldInvalidateOnError && config.getInvalidationKey) {
          queryClient.invalidateQueries({
            queryKey: config.getInvalidationKey(params),
          });
        }

        notifications.show({
          ...ErrorNotification,
          title: 'Error',
          message: `${config.errorMessage}: ${error.message}`,
        });
      },
    });
  };
}

/**
 * Creates a simple mutation hook with only notifications (no cache invalidation).
 */
export function createSimpleMutation<TParams, TResult = void>(config: {
  mutationFn: (client: LabourServiceClient, params: TParams) => Promise<ApiResponse<TResult>>;
  successMessage: string;
  errorMessage: string;
}) {
  return function useCreatedMutation(client: LabourServiceClient) {
    return useMutation({
      mutationFn: async (params: TParams) => {
        const response = await config.mutationFn(client, params);

        if (!response.success) {
          throw new Error(response.error || config.errorMessage);
        }

        return response.data as TResult;
      },

      onSuccess: () => {
        notifications.show({
          ...Success,
          title: 'Success',
          message: config.successMessage,
        });
      },

      onError: (error: Error) => {
        notifications.show({
          ...ErrorNotification,
          title: 'Error',
          message: `${config.errorMessage}: ${error.message}`,
        });
      },
    });
  };
}
