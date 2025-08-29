import {
  ApiError,
  SendSubscriberInviteRequest,
  SubscriberService,
  UserService,
} from '@clients/labour_service';
import { Error as ErrorNotification, Success } from '@shared/Notifications';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { notifications } from '@mantine/notifications';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for fetching current subscriber data
 */
export function useSubscriber() {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.subscriber.user(user?.profile.sub || ''),
    queryFn: async () => {
      try {
        const response = await UserService.getUser();
        return response;
      } catch (err) {
        throw new Error('Failed to load subscriber data. Please try again later.');
      }
    },
    enabled: !!user?.profile.sub,
  });
}

/**
 * Custom hook for updating subscriber information
 */
export function useUpdateSubscriber() {
  const { user } = useApiAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      // This would need to be implemented based on your actual API
      throw new Error('Update subscriber functionality not yet implemented in API');
    },
    onSuccess: () => {
      // Invalidate subscriber query to fetch updated data
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriber.user(user?.profile.sub || ''),
      });

      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Profile updated successfully',
      });
    },
    onError: (error: Error) => {
      notifications.show({
        ...ErrorNotification,
        title: 'Error',
        message: `Failed to update profile: ${error.message}`,
      });
    },
  });
}

/**
 * Custom hook for sending subscriber invites
 */
export function useSendSubscriberInvite() {
  return useMutation({
    mutationFn: async (email: string) => {
      const requestBody: SendSubscriberInviteRequest = { invite_email: email };
      await SubscriberService.sendInvite({ requestBody });
    },
    onSuccess: () => {
      notifications.show({
        ...Success,
        title: 'Success',
        message: 'Invite email sent',
      });
    },
    onError: (err) => {
      if (err instanceof ApiError && err.status === 429) {
        notifications.show({
          ...ErrorNotification,
          title: 'Slow down!',
          message: 'You have sent too many invites today. Wait until tomorrow to send more.',
        });
      } else {
        notifications.show({
          ...ErrorNotification,
          title: 'Error Sending Invite',
          message: 'Something went wrong. Please try again.',
        });
      }
    },
  });
}
