import { ApiError, CreateCheckoutRequest, PaymentsService } from '@clients/labour_service';
import { Error as ErrorNotification } from '@shared/Notifications';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for creating Stripe checkout sessions
 */
export function useCreateCheckoutSession() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      subscriptionId,
      successUrl,
      cancelUrl,
    }: {
      subscriptionId: string;
      successUrl: string;
      cancelUrl: string;
    }) => {
      const requestBody: CreateCheckoutRequest = {
        upgrade: 'supporter',
        subscription_id: subscriptionId,
        success_url: successUrl,
        cancel_url: cancelUrl,
      };
      return await PaymentsService.createCheckoutSession({ requestBody });
    },
    onSuccess: async (data) => {
      window.location.href = data.url!;
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.user(user?.sub || '') });
    },
    onError: async (error) => {
      let message = 'Unknown error occurred';
      if (error instanceof ApiError) {
        try {
          const body = error.body as { description: string };
          message = body.description;
        } catch {
          // Fallback to default message
        }
      }
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message,
      });
    },
  });
}
