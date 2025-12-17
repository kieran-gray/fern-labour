import type { CreateContactMessageRequest } from '@clients/contact_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useMutation } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { useContactClient } from './useContactClient';

export function useSubmitContactForm() {
  const client = useContactClient();

  return useMutation({
    mutationFn: async (request: CreateContactMessageRequest) => {
      const response = await client.createContactMessage(request);
      if (!response.success) {
        throw new Error(response.error || 'Failed to send message');
      }
      return response;
    },
    onSuccess: () => {
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Your message has been sent successfully. We will get back to you soon!',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to send message: ${error.message}`,
      });
    },
  });
}
