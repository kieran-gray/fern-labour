import {
  ContactUsSendMessageApiV1ContactUsPostData,
  ContactUsService,
} from '@clients/contact_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useMutation } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for submitting contact form
 */
export function useSubmitContactForm() {
  useApiAuth(); // Ensure API authentication is set up

  return useMutation({
    mutationFn: async (requestBody: ContactUsSendMessageApiV1ContactUsPostData['requestBody']) => {
      const response = await ContactUsService.contactUsSendMessage({ requestBody });
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
