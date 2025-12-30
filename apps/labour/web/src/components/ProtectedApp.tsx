import { useEffect, useRef, type ReactNode } from 'react';
import { useClerkUser } from '@base/hooks/useClerkUser';
import { useNetworkState } from '@base/offline/sync/networkDetector';
import { RedirectToSignIn, useAuth } from '@clerk/clerk-react';
import { PageLoading } from './PageLoading/PageLoading';

interface ProtectedAppProps {
  children: ReactNode;
}

export const ProtectedApp: React.FC<ProtectedAppProps> = (props) => {
  const { children } = props;

  const { isOnline } = useNetworkState();
  const { isLoaded: isAuthLoaded, isSignedIn, getToken } = useAuth();
  const { user, isLoaded: isUserLoaded } = useClerkUser();
  const wasOnlineRef = useRef<boolean | null>(null);

  // Handle reconnection - refresh token when coming back online
  useEffect(() => {
    if (wasOnlineRef.current === null) {
      wasOnlineRef.current = isOnline;
      return;
    }

    const cameOnline = wasOnlineRef.current === false && isOnline === true;
    wasOnlineRef.current = isOnline;

    if (!cameOnline) {
      return;
    }

    if (user || isSignedIn) {
      getToken({ skipCache: true }).catch(() => {
        // Token refresh failed, user will be redirected to sign in
      });
    }
  }, [isOnline, user, isSignedIn, getToken]);

  // Handle offline mode with cached user
  if (!isOnline && user) {
    return children;
  }

  // Show loading while auth state is being determined
  if (!isAuthLoaded || !isUserLoaded) {
    return <PageLoading />;
  }

  // If signed in, show the app
  if (isSignedIn) {
    return children;
  }

  // Not signed in, redirect to sign in
  return <RedirectToSignIn />;
};
