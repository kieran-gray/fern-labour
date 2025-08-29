import { useEffect } from 'react';
import { OpenAPI as ContactServiceAPI } from '@clients/contact_service';
import { OpenAPI as LabourServiceAPI } from '@clients/labour_service';
import { useAuth } from 'react-oidc-context';

/**
 * Custom hook that automatically sets up API authentication tokens
 * for both Labour Service and Contact Service clients.
 *
 * This hook should be used in components that make API calls.
 * It automatically updates the OpenAPI TOKEN configuration when
 * the user's authentication state changes.
 */
export function useApiAuth() {
  const auth = useAuth();

  useEffect(() => {
    // Set up token function for both API clients
    const tokenProvider = async () => {
      return auth.user?.access_token || '';
    };

    // Configure both service clients
    LabourServiceAPI.TOKEN = tokenProvider;
    ContactServiceAPI.TOKEN = tokenProvider;
  }, [auth.user?.access_token]);

  // Return auth state for convenience
  return {
    isAuthenticated: auth.isAuthenticated,
    isLoading: auth.isLoading,
    user: auth.user,
    accessToken: auth.user?.access_token,
  };
}
