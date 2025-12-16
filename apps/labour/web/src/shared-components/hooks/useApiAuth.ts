import { useEffect } from 'react';
import { useAuth } from '@clerk/clerk-react';
import { OpenAPI as ContactServiceAPI } from '@clients/contact_service';
import { OpenAPI as LabourServiceAPI } from '@clients/labour_service';
import { useClerkUser } from './useClerkUser';

/**
 * Custom hook that automatically sets up API authentication tokens
 * for both Labour Service and Contact Service clients.
 *
 * This hook should be used in components that make API calls.
 * It automatically updates the OpenAPI TOKEN configuration when
 * the user's authentication state changes.
 */
export function useApiAuth() {
  const { isLoaded: isAuthLoaded, isSignedIn, getToken } = useAuth();
  const { user, isLoaded: isUserLoaded } = useClerkUser();

  useEffect(() => {
    // Set up token function for both API clients
    const tokenProvider = async () => {
      // Return cached token or fetch new one
      try {
        if (isSignedIn) {
          const token = await getToken();
          return token || '';
        }
      } catch (error) {
        console.error('Failed to get access token:', error);
      }

      return '';
    };

    // Configure both service clients
    LabourServiceAPI.TOKEN = tokenProvider;
    ContactServiceAPI.TOKEN = tokenProvider;
  }, [isSignedIn, getToken]);

  // Return auth state for convenience
  return {
    isAuthenticated: isSignedIn,
    isLoading: !isAuthLoaded || !isUserLoaded,
    user,
    accessToken: null, // Access token is fetched dynamically via getToken
  };
}
