import { useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { useNetworkState } from '@base/offline/sync/networkDetector.ts';
import { hasAuthParams, useAuth } from 'react-oidc-context';
import { ErrorContainer } from './ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from './PageLoading/PageLoading.tsx';

interface ProtectedAppProps {
  children: ReactNode;
}

export const ProtectedApp: React.FC<ProtectedAppProps> = (props) => {
  const { children } = props;

  const { isOnline } = useNetworkState();
  const auth = useAuth();
  const [hasTriedSignin, setHasTriedSignin] = useState(false);
  const wasOnlineRef = useRef<boolean | null>(null);
  const isSilentRedirectRoute = useMemo(() => window.location.pathname === '/silent-redirect', []);

  /**
   * Do auto sign in.
   *
   * See {@link https://github.com/authts/react-oidc-context?tab=readme-ov-file#automatic-sign-in}
   */
  useEffect(() => {
    if (isSilentRedirectRoute) {
      return;
    }

    if (
      !(
        hasAuthParams() ||
        auth.isAuthenticated ||
        auth.activeNavigator ||
        auth.isLoading ||
        hasTriedSignin
      )
    ) {
      void auth.signinRedirect();
      setHasTriedSignin(true);
    }
  }, [auth, hasTriedSignin, isSilentRedirectRoute]);

  useEffect(() => {
    if (isSilentRedirectRoute) {
      return;
    }
    if (wasOnlineRef.current === null) {
      wasOnlineRef.current = isOnline;
      return;
    }

    const cameOnline = wasOnlineRef.current === false && isOnline === true;
    wasOnlineRef.current = isOnline;

    if (!cameOnline) {
      return;
    }

    if (auth.user || auth.isAuthenticated) {
      auth.signinSilent().catch(() => {
        void auth.signinRedirect();
      });
      return;
    }

    if (!auth.activeNavigator && !auth.isLoading) {
      void auth.signinRedirect();
    }
  }, [isOnline, auth, isSilentRedirectRoute]);

  if (!isSilentRedirectRoute && auth.error) {
    if (auth.error?.message.includes('No matching state')) {
      window.location.href = '/';
      return <PageLoading />;
    }

    if (!isOnline && auth.user) {
      // User exists in storage, allow access in offline mode
      return children;
    }

    return <ErrorContainer message={auth.error?.message} />;
  }

  if (!isSilentRedirectRoute && auth.isLoading) {
    return <PageLoading />;
  }

  if (isSilentRedirectRoute || auth.isAuthenticated) {
    return children;
  }

  return <ErrorContainer message="Unable to sign in" />;
};
