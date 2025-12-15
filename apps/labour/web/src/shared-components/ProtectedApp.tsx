import { useEffect, useRef, type ReactNode } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { useNetworkState } from '@base/offline/sync/networkDetector';
import { ErrorContainer } from './ErrorContainer/ErrorContainer';
import { PageLoading } from './PageLoading/PageLoading';

interface ProtectedAppProps {
  children: ReactNode;
}

export const ProtectedApp: React.FC<ProtectedAppProps> = (props) => {
  const { children } = props;

  const { isOnline } = useNetworkState();
  const { isAuthenticated, isLoading, error, user, loginWithRedirect, getAccessTokenSilently } =
    useAuth0();
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

    if (user || isAuthenticated) {
      getAccessTokenSilently({ cacheMode: 'off' }).catch(() => {
        void loginWithRedirect();
      });
      return;
    }

    if (!isLoading) {
      void loginWithRedirect();
    }
  }, [isOnline, user, isAuthenticated, isLoading, getAccessTokenSilently, loginWithRedirect]);

  if (error) {
    if (error?.message.includes('No matching state') || error?.message.includes('state mismatch')) {
      window.location.href = '/';
      return <PageLoading />;
    }

    if (!isOnline && user) {
      return children;
    }

    return <ErrorContainer message={error?.message} />;
  }

  if (isLoading) {
    return <PageLoading />;
  }

  if (isAuthenticated) {
    return children;
  }

  if (!isLoading) {
    void loginWithRedirect();
  }

  return <PageLoading />;
};
