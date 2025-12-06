import { QueryClient } from '@tanstack/react-query';

const auth0Domain = import.meta.env.VITE_AUTH0_DOMAIN;
const auth0Audience = import.meta.env.VITE_AUTH0_AUDIENCE;
const auth0ClientId = import.meta.env.VITE_AUTH0_CLIENT_ID;

export const auth0Config = {
  domain: auth0Domain,
  clientId: auth0ClientId,
  audience: auth0Audience,
  redirectUri: window.location.origin,
  logoutRedirectUri: import.meta.env.VITE_POST_LOGOUT_REDIRECT || `${window.location.origin}/`,
};

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 24 * 60 * 60 * 1000,

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

      refetchOnWindowFocus: false,
      refetchOnMount: true,
      refetchOnReconnect: true,
      networkMode: 'always',
    },
    mutations: {
      retry: (failureCount, error: any) => {
        if (error?.name === 'NetworkError' || !navigator.onLine) {
          return false;
        }
        if (error?.status >= 500) {
          return failureCount < 2;
        }
        return false;
      },
      networkMode: 'always',
    },
  },
});
