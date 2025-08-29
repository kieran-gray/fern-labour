import { LabourService } from '@clients/labour_service';
import { useQuery } from '@tanstack/react-query';
import { queryKeys } from './queryKeys';
import { useApiAuth } from './useApiAuth';

/**
 * Custom hook for fetching subscription token for sharing
 */
export function useSubscriptionToken() {
  const { user } = useApiAuth();

  return useQuery({
    queryKey: queryKeys.token.user(user?.profile.sub || ''),
    queryFn: async () => {
      try {
        const response = await LabourService.getSubscriptionToken();
        return response.token;
      } catch (err) {
        throw new Error('Failed to load subscription token. Please try again later.');
      }
    },
    enabled: !!user?.profile.sub,
  });
}
