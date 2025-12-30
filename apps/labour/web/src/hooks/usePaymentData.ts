import type { LabourServiceClient } from '@base/clients/labour_service';
import { Error as ErrorNotification } from '@components/Notifications';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { queryKeys } from './queryKeys';

export function useCreateCheckoutSession(client: LabourServiceClient) {
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
      const response = await client.createCheckoutSession({
        subscription_id: subscriptionId,
        success_url: successUrl,
        cancel_url: cancelUrl,
      });

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to create checkout session');
      }

      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.all,
      });

      window.location.href = data.url;
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to create checkout session: ${error.message}`,
      });
    },
  });
}
