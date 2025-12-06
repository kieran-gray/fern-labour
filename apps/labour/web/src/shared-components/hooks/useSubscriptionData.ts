import {
  ApiError,
  SubscribeToRequest,
  SubscriptionManagementService,
  SubscriptionService,
  UpdateContactMethodsRequest,
} from '@clients/labour_service';
import { Error as ErrorNotification } from '@shared/Notifications';
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
    queryKey: queryKeys.subscriptions.subscriber(user?.sub || ''),
    queryFn: async () => {
      try {
        const response = await SubscriptionService.getSubscriberSubscriptions();
        return response;
      } catch (err) {
        throw new Error('Failed to load subscriptions. Please try again later.');
      }
    },
    enabled: !!user?.sub,
    refetchOnMount: 'always',
  });
}

/**
 * Custom hook for fetching labour subscriptions
 * Used by labour owners to view who is subscribed to their labour
 */
export function useLabourSubscriptions(labourId: string) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.subscriptions.labour(user?.sub || ''),
    queryFn: async () => {
      try {
        const response = await SubscriptionService.getLabourSubscriptions({ labourId });
        return response;
      } catch (err) {
        throw new Error('Failed to load labour subscriptions. Please try again later.');
      }
    },
    enabled: !!user?.sub,
    refetchOnMount: 'always',
  });
}

/**
 * Custom hook for fetching subscription data by ID
 * Used for viewing detailed subscription information
 */
export function useSubscriptionById(subscriptionId: string) {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.subscriptions.byId(subscriptionId, user?.sub || ''),
    queryFn: async () => {
      try {
        const response = await SubscriptionService.getSubscriptionById({ subscriptionId });
        return response;
      } catch (err) {
        if (err instanceof ApiError && [403, 404].includes(err.status)) {
          throw new Error('Subscription not found');
        }
        throw new Error('Failed to load subscription data. Please try again later.');
      }
    },
    enabled: !!subscriptionId && !!user?.sub,
    refetchOnMount: 'always',
  });
}

/**
 * Custom hook for subscriber subscribing to labour
 */
export function useSubscribeTo() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (request: { labourId: string; requestBody: SubscribeToRequest }) => {
      const response = await SubscriptionService.subscribeTo({
        labourId: request.labourId,
        requestBody: request.requestBody,
      });
      return response.subscription;
    },
    onSuccess: (subscription) => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.subscriber(user?.sub || ''),
      });
      queryClient.setQueryData(['subscription', subscription.id, user?.sub], subscription);
    },
    onError: () => {
      // Generic error
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Token or Labour ID is incorrect.`,
      });
    },
  });
}

/**
 * Custom hook for updating subscription contact methods
 */
export function useUpdateContactMethods() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (requestBody: UpdateContactMethodsRequest) => {
      const response = await SubscriptionManagementService.updateContactMethods({ requestBody });
      return response.subscription;
    },
    onSuccess: (subscription) => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.byId(subscription.id, user?.sub || ''),
      });
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.subscriber(user?.sub || ''),
      });
      queryClient.setQueryData(
        queryKeys.subscriptions.byId(subscription.id, user?.sub || ''),
        subscription
      );
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
 * Custom hook for unsubscribing from a labour
 */
export function useUnsubscribeFrom() {
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
        queryKey: queryKeys.subscriptions.subscriber(user?.sub || ''),
      });
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.labour(user?.sub || ''),
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to unsubscribe: ${error.message}`,
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
        queryKey: queryKeys.subscriptions.labour(user?.sub || ''),
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
        queryKey: queryKeys.subscriptions.labour(user?.sub || ''),
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
        queryKey: queryKeys.subscriptions.labour(user?.sub || ''),
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
        queryKey: queryKeys.subscriptions.labour(user?.sub || ''),
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
