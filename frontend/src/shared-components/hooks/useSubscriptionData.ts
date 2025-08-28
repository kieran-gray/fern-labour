import {
  ApiError,
  SubscribeToApiV1SubscriptionSubscribeLabourIdPostData,
  SubscriptionManagementService,
  SubscriptionService,
} from '@clients/labour_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for fetching subscriber subscriptions
 * Used by subscribers to view their subscriptions
 */
export function useSubscriberSubscriptions() {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.subscriptions.subscriber(user?.profile.sub || ''),
    queryFn: async () => {
      try {
        const response = await SubscriptionService.getSubscriberSubscriptions();
        return response;
      } catch (err) {
        throw new Error('Failed to load subscriptions. Please try again later.');
      }
    },
    enabled: !!user?.profile.sub,
  });
}

/**
 * Custom hook for fetching labour subscriptions
 * Used by labour owners to view who is subscribed to their labour
 */
export function useLabourSubscriptions(labourId: string) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
    queryFn: async () => {
      try {
        const response = await SubscriptionService.getLabourSubscriptions({ labourId });
        return response;
      } catch (err) {
        throw new Error('Failed to load labour subscriptions. Please try again later.');
      }
    },
    enabled: !!user?.profile.sub,
  });
}

/**
 * Custom hook for fetching subscription data by ID
 * Used for viewing detailed subscription information
 */
export function useSubscriptionById(subscriptionId: string) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.subscriptions.byId(subscriptionId, user?.profile.sub || ''),
    queryFn: async () => {
      try {
        const response = await SubscriptionService.getSubscriptionById({ subscriptionId });
        return response;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          throw new Error('Subscription not found');
        }
        throw new Error('Failed to load subscription data. Please try again later.');
      }
    },
    enabled: !!subscriptionId && !!user?.profile.sub,
  });
}

/**
 * Custom hook for creating a subscription
 */
export function useCreateSubscription() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (request: {
      labourId: string;
      requestBody: SubscribeToApiV1SubscriptionSubscribeLabourIdPostData['requestBody'];
    }) => {
      const response = await SubscriptionService.subscribeTo({
        labourId: request.labourId,
        requestBody: request.requestBody,
      });
      return response;
    },
    onSuccess: () => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.subscriber(user?.profile.sub || ''),
      });
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Subscription created successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to create subscription: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for updating subscription contact methods
 */
export function useUpdateSubscription() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (request: { subscriptionId: string; requestBody: any }) => {
      const response = await SubscriptionManagementService.updateContactMethods({
        requestBody: {
          subscription_id: request.subscriptionId,
          ...request.requestBody,
        },
      });
      return response;
    },
    onSuccess: (_, { subscriptionId }) => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.byId(subscriptionId, user?.profile.sub || ''),
      });
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.subscriber(user?.profile.sub || ''),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Contact methods updated successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to update contact methods: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for deleting a subscription
 */
export function useDeleteSubscription() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (labourId: string) => {
      await SubscriptionService.unsubscribeFrom({
        requestBody: { labour_id: labourId },
      });
    },
    onSuccess: () => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.subscriber(user?.profile.sub || ''),
      });
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Subscription removed successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to remove subscription: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for approving a subscriber
 */
export function useApproveSubscriber() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (subscriptionId: string) => {
      await SubscriptionManagementService.approveSubscriber({
        requestBody: { subscription_id: subscriptionId },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to accept subscription: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for removing a subscriber
 */
export function useRemoveSubscriber() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (subscriptionId: string) => {
      await SubscriptionManagementService.removeSubscriber({
        requestBody: { subscription_id: subscriptionId },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to remove subscriber: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for blocking a subscriber
 */
export function useBlockSubscriber() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (subscriptionId: string) => {
      await SubscriptionManagementService.blockSubscriber({
        requestBody: { subscription_id: subscriptionId },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to block subscriber: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for unblocking a subscriber
 */
export function useUnblockSubscriber() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (subscriptionId: string) => {
      await SubscriptionManagementService.unblockSubscriber({
        requestBody: { subscription_id: subscriptionId },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.profile.sub || ''),
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to unblock subscriber: ${error.message}`,
      });
    },
  });
}
