import type { LabourServiceV2Client } from '@clients/labour_service_v2';
import { Error as ErrorNotification } from '@shared/Notifications';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { queryKeysV2 } from './useLabourDataV2';

export function useCreateCheckoutSessionV2(client: LabourServiceV2Client) {
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
        queryKey: queryKeysV2.subscriptions.all,
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
