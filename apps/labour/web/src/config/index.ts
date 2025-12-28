import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 30 * 60 * 1000,

      retry: (failureCount, error: any) => {
        if (error?.status >= 400 && error?.status < 500) {
          if (error?.status === 408 || error?.status === 429) {
            return failureCount < 3;
          }
          return false;
        }
        return failureCount < 3;
      },

      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),

      refetchOnWindowFocus: true,
      refetchOnMount: true,
      refetchOnReconnect: true,
      networkMode: 'always',
    },
    mutations: {
      // Pause mutations when offline, automatically retry when back online
      networkMode: 'offlineFirst',
      retry: (failureCount, error: any) => {
        // Don't retry client errors (except timeout/rate limit)
        if (error?.status >= 400 && error?.status < 500) {
          if (error?.status === 408 || error?.status === 429) {
            return failureCount < 3;
          }
          return false;
        }
        // Retry server errors
        if (error?.status >= 500) {
          return failureCount < 2;
        }
        return false;
      },
    },
  },
});
