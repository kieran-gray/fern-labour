import { useAuth } from '@clerk/clerk-react';
import { useClerkUser } from './useClerkUser';

export function useApiAuth() {
  const { isLoaded: isAuthLoaded, isSignedIn } = useAuth();
  const { user, isLoaded: isUserLoaded } = useClerkUser();

  return {
    isAuthenticated: isSignedIn,
    isLoading: !isAuthLoaded || !isUserLoaded,
    user,
    accessToken: null,
  };
}
